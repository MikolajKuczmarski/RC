import pygame
import os
import numpy as np
import time
import asyncio
import shutil  # Dodano do kopiowania plików
from PIL import Image

# Konfiguracja programu
IMAGE_FOLDER = "sinusoidal_noise_scaled"
OUTPUT_FOLDER = "results"
CROSS_DURATION = 1000  # ms (1 sekunda)
BASE_IMAGE_SIZE = 300  # Bazowy rozmiar obrazów (kwadratowy)
IMAGE_SCALE_FACTOR = 0.2  # Skala obrazów względem szerokości okna

# Tworzenie katalogu na wyniki
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Inicjalizacja Pygame
pygame.init()
screen_info = pygame.display.Info()
screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h), pygame.RESIZABLE)
pygame.display.set_caption("Reversed Correlation Experiment")
font = pygame.font.Font(pygame.font.match_font('arial'), 40)

def get_scaled_size():
    width, height = screen.get_size()
    new_size = int(width * IMAGE_SCALE_FACTOR)
    return (new_size, new_size)



async def show_cross():
    screen.fill((255, 255, 255))
    text = font.render("+", True, (0, 0, 0))
    text_rect = text.get_rect(center=(screen.get_width()//2, screen.get_height()//2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    await asyncio.sleep(1)

async def show_start_page():
    running = True
    while running:
        screen.fill((255, 255, 255))
        title_font = pygame.font.Font(pygame.font.match_font('arial'), 40)
        text_lines = [
            "Dziękuję za udział w badaniu.",
            "Za chwilę poprosimy Cię o ocenienie serii obrazów twarzy",
            "pod względem określonej cechy.",
            "Jeśli jesteś gotowy/gotowa, przejdź do następnego kroku."
        ]
        
        text_y = screen.get_height() // 3
        for line in text_lines:
            text_surface = title_font.render(line, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(screen.get_width() // 2, text_y))
            screen.blit(text_surface, text_rect)
            text_y += 60

        button_font = pygame.font.Font(pygame.font.match_font('arial'), 20)
        button_width, button_height = 200, 50
        quit_button = pygame.Rect((screen.get_width() // 2 - 220, screen.get_height() - 250), (button_width, button_height))
        next_button = pygame.Rect((screen.get_width() // 2 + 20, screen.get_height() - 250), (button_width, button_height))
        
        pygame.draw.rect(screen, (255, 255, 255), quit_button, border_radius=10)
        pygame.draw.rect(screen, (0, 0, 0), quit_button, 2, border_radius=10)
        pygame.draw.rect(screen, (20, 20, 20), next_button, border_radius=10)
        
        quit_text = button_font.render("Zrezygnuj", True, (0, 0, 0))
        next_text = button_font.render("Dalej", True, (255, 255, 255))
        screen.blit(quit_text, quit_text.get_rect(center=quit_button.center))
        screen.blit(next_text, next_text.get_rect(center=next_button.center))
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    exit()
                elif next_button.collidepoint(event.pos):
                    running = False


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False

        await asyncio.sleep(0)

async def show_end_page():
    running = True
    while running:
        screen.fill((255, 255, 255))
        title_font = pygame.font.Font(pygame.font.match_font('arial'), 40)
        text_lines = [
            "Dziękuję za udział w badaniu.",
            "Możesz zamknąć przeglądarkę."
        ]
        
        text_y = screen.get_height() // 3
        for line in text_lines:
            text_surface = title_font.render(line, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(screen.get_width() // 2, text_y))
            screen.blit(text_surface, text_rect)
            text_y += 60

        
        pygame.display.flip()
        await asyncio.sleep(0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


async def show_choice_page():
    runs = sorted([d for d in os.listdir(IMAGE_FOLDER) if d.startswith("run_")])
    run_index = 0

    running = True
    while running and run_index < len(runs):
        run_folder = os.path.join(IMAGE_FOLDER, runs[run_index])
        folder_number = run_folder.split("_")[-1]  # Pobranie numeru folderu
        print(f"Brak pliku pomijam...")
        blended_file = os.path.join(run_folder, f"blended_run_{folder_number}.png")
        blended_inverse_file = os.path.join(run_folder, f"blended_inverse_run_{folder_number}.png")
        
        if not os.path.exists(blended_file) or not os.path.exists(blended_inverse_file):
            print(f"Brak pliku: {blended_file} lub {blended_inverse_file}, pomijam...")
            run_index += 1
            continue
        
        left_image = pygame.image.load(blended_file)
        right_image = pygame.image.load(blended_inverse_file)
        new_size = get_scaled_size()
        left_image = pygame.transform.scale(left_image, new_size)
        right_image = pygame.transform.scale(right_image, new_size)
        
        left_x = screen.get_width() // 2 - new_size[0] - 20
        right_x = screen.get_width() // 2 + 20
        y_pos = screen.get_height() // 2 - new_size[1] // 2
        
        screen.fill((255, 255, 255))
        screen.blit(left_image, (left_x, y_pos))
        screen.blit(right_image, (right_x, y_pos))
        pygame.display.flip()
        await asyncio.sleep(0)

        
        choice_made = False
        while not choice_made:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        
                        choice_made = True
                    elif event.key == pygame.K_RIGHT:
                    
                        choice_made = True
                    run_index += 1
                    await show_cross()

            await asyncio.sleep(0)


async def main():
    await show_start_page()
    await show_choice_page()
    await show_end_page()

   


asyncio.run(main())
