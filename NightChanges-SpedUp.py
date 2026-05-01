import sys
from time import sleep
import time
import os
import shutil

os.system('cls' if os.name == 'nt' else 'clear')

# ── ANSI color codes ──────────────────────────────────────────────────────────
RESET       = "\033[0m"
BOLD        = "\033[1m"
DIM         = "\033[2m"

# Spotify-ish palette
GREEN       = "\033[38;2;30;215;96m"    # spotify green  → active line
WHITE_BRIGHT= "\033[38;2;255;255;255m"  # putih terang   → baris habis diketik
GRAY        = "\033[38;2;80;80;80m"     # abu gelap      → baris lama (dimmed)
CURSOR_CLR  = "\033[38;2;30;215;96m"    # sama kayak green

def hide_cursor():
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

def show_cursor():
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()

def move_cursor(row, col):
    sys.stdout.write(f"\033[{row};{col}H")
    sys.stdout.flush()

def clear_screen():
    sys.stdout.write("\033[2J")
    sys.stdout.flush()

def get_terminal_width():
    return shutil.get_terminal_size().columns

def get_terminal_height():
    return shutil.get_terminal_size().lines

def center_text(text, width):
    """Return left-pad agar teks center di terminal."""
    visible_len = len(text)
    pad = max(0, (width - visible_len) // 2)
    return " " * pad

# ── Lyrics data ───────────────────────────────────────────────────────────────
LYRICS = [
    ("Everything that you've ever dreamed of", 0.07),
    ("Disappearing when you wake up",          0.088),
    ("But there's nothing to be",              0.076),
    ("Afraid of",                              0.09),
    ("Even when the night",                    0.076),
    ("Changes",                                0.08),
    ("It will never change",                   0.076),
    ("Baby",                                   0.08),
    ("It will never change",                   0.076),
    ("Baby",                                   0.08),
    ("It will never change",                   0.076),
    ("Me and you",                             0.12),
]

DELAYS = [0.6, 0.7, 0.2, 0.6, 0.6, 1, 0.6, 0.9, 0.6, 0.9, 0.9, 0.9]

SONG_TITLE  = "Night Changes"
SONG_ARTIST = "One Direction"

# ── Render state (simpan semua baris yg sudah selesai) ────────────────────────
rendered_lines = []   # list of (text, color)

def redraw(term_w, term_h):
    """Gambar ulang semua baris dari atas."""
    clear_screen()

    # ── Header ──
    move_cursor(1, 1)
    title_pad  = center_text(SONG_TITLE, term_w)
    artist_pad = center_text(SONG_ARTIST, term_w)
    sys.stdout.write(f"{title_pad}{BOLD}{WHITE_BRIGHT}{SONG_TITLE}{RESET}\n")
    sys.stdout.write(f"{artist_pad}{DIM}{GRAY}{SONG_ARTIST}{RESET}\n")
    sys.stdout.write("\n")

    # ── Lyrics baris yang sudah dirender ──
    for text, color in rendered_lines:
        pad = center_text(text, term_w)
        sys.stdout.write(f"{pad}{color}{text}{RESET}\n")

    sys.stdout.flush()

def print_lyrics_synced():
    hide_cursor()
    term_w = get_terminal_width()
    term_h = get_terminal_height()

    # Gambar header dulu
    redraw(term_w, term_h)

    for i, (line, char_delay) in enumerate(LYRICS):
        # Hitung posisi baris aktif di layar
        # Header = 3 baris (title + artist + blank), lalu lyrics mulai
        active_row = 4 + len(rendered_lines) + 1   # +1 karena 1-indexed

        pad = center_text(line, term_w)

        # ── Typewriter effect dengan warna hijau (aktif) ──
        move_cursor(active_row, 1)
        sys.stdout.write(pad)
        for char in line:
            sys.stdout.write(f"{GREEN}{BOLD}{char}{RESET}")
            sys.stdout.flush()
            sleep(char_delay)

        # ── Setelah selesai diketik → simpan sebagai "done" ──
        # Baris terakhir = putih terang, sebelumnya = dimmed gray
        done_color = WHITE_BRIGHT
        rendered_lines.append((line, done_color))

        # Redim semua baris sebelumnya
        updated = []
        for j, (t, _) in enumerate(rendered_lines):
            if j == len(rendered_lines) - 1:
                updated.append((t, WHITE_BRIGHT))   # baris yg baru selesai
            else:
                updated.append((t, GRAY))            # baris lama → abu
        rendered_lines.clear()
        rendered_lines.extend(updated)

        # Redraw biar warna ter-update
        redraw(term_w, term_h)

        # Delay antar baris
        time.sleep(DELAYS[i])

    # ── Selesai: semua baris jadi putih terang ──
    final = [(t, WHITE_BRIGHT) for t, _ in rendered_lines]
    rendered_lines.clear()
    rendered_lines.extend(final)
    redraw(term_w, term_h)

    # Pindah cursor ke bawah lyrics
    move_cursor(4 + len(rendered_lines) + 2, 1)
    show_cursor()

print_lyrics_synced()