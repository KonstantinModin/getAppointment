# from plyer import notification
import pygame

# def notify_popup():
#     notification.notify(
#         title="Website Checker",
#         message="✅ Appointment available!",
#         timeout=10  # seconds
#     )

def playAlert():
    pygame.mixer.init()
    sound = pygame.mixer.Sound('alert.mp3')
    sound.play(loops=-1)