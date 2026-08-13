#include "raylib.h"
#include <stdlib.h>
#include <math.h>

#define WIDTH 800
#define HEIGHT 400
#define GRID_SIZE 4 // Size of each visual grid cell

// 1. Simple 2D Smooth Value Noise Implementation
float Hash(int x, int y, int seed) {
    int n = x + y * 57 + seed * 131;
    n = (n << 13) ^ n;
    return (1.0f - ((n * (n * n * 15731 + 789221) + 1376312589) & 0x7fffffff) / 1073741824.0f);
}

float Lerp(float a, float b, float t) { return a + t * (b - a); }

// Renamed from Fade to SmoothFade to avoid conflict with raylib's Fade()
float SmoothFade(float t) { return t * t * t * (t * (t * 6 - 15) + 10); }

float SmoothNoise2D(float x, float y, int seed) {
    int X = (int)floorf(x);
    int Y = (int)floorf(y);
    float xf = x - floorf(x);
    float yf = y - floorf(y);

    float u = SmoothFade(xf);
    float v = SmoothFade(yf);

    float n00 = (Hash(X, Y, seed) + 1.0f) * 0.5f;
    float n10 = (Hash(X + 1, Y, seed) + 1.0f) * 0.5f;
    float n01 = (Hash(X, Y + 1, seed) + 1.0f) * 0.5f;
    float n11 = (Hash(X + 1, Y + 1, seed) + 1.0f) * 0.5f;

    float x1 = Lerp(n00, n10, u);
    float x2 = Lerp(n01, n11, u);

    return Lerp(x1, x2, v);
}

// 2. Generate and Render the Map
void DrawWorld(int seed) {
    float scale = 0.02f; // Controls how "zoomed in" the continents are

    for (int y = 0; y < HEIGHT; y += GRID_SIZE) {
        for (int x = 0; x < WIDTH; x += GRID_SIZE) {

            // Generate multilayer organic noise
            float n = SmoothNoise2D(x * scale, y * scale, seed) * 0.7f +
                      SmoothNoise2D(x * scale * 2, y * scale * 2, seed) * 0.3f;

            Color tileColor;
            bool isLand = false;

            // Define Biome Palette
            if (n < 0.42f) {
                tileColor = (Color){ 75, 85, 135, 255 };  // Muted Navy Water
            } else if (n < 0.48f) {
                tileColor = (Color){ 210, 190, 140, 255 }; // Sandy Coast
                isLand = true;
            } else if (n < 0.62f) {
                tileColor = (Color){ 145, 185, 110, 255 }; // Light Meadow Green
                isLand = true;
            } else {
                tileColor = (Color){ 80, 135, 85, 255 };  // Forest Green
                isLand = true;
            }

            // Draw the background color cell
            DrawRectangle(x, y, GRID_SIZE, GRID_SIZE, tileColor);

            // Scatter black dots using a stable grid coordinate check
            if (isLand) {
                unsigned int dotHash = (x * 739221 + y * 1376312589 + seed) % 100;
                if (dotHash < 5) { // 5% coverage
                    DrawRectangle(x + GRID_SIZE/2, y + GRID_SIZE/2, 1, 1, (Color){ 20, 25, 20, 255 });
                }
            }
        }
    }
}

// 3. Main Loop
int main(void) {
    InitWindow(WIDTH, HEIGHT, "Procedural 2D Map Generator");
    SetTargetFPS(60);

    int currentSeed = 42;

    while (!WindowShouldClose()) {
        if (IsKeyPressed(KEY_SPACE)) {
            currentSeed = GetRandomValue(0, 100000);
        }

        BeginDrawing();
            ClearBackground(BLACK);
            DrawWorld(currentSeed);
            DrawRectangle(10, 10, 310, 35, (Color){ 0, 0, 0, 180 });
            DrawText("Press SPACE to generate a new world", 15, 15, 16, WHITE);
        EndDrawing();
    }

    CloseWindow();
    return 0;
}