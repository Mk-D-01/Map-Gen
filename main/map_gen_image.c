

// =============================================================================
// FILE 1: map_gen.c
// Original procedural map — renders to a live window (requires display)
// Compile: gcc map_gen.c -o map_gen -lraylib -lm -lpthread -ldl
// Run:     ./map_gen          (press SPACE to generate a new world)
// =============================================================================

/*
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
float Fade(float t) { return t * t * t * (t * (t * 6 - 15) + 10); }

float SmoothNoise2D(float x, float y, int seed) {
    int X = (int)floorf(x);
    int Y = (int)floorf(y);
    float xf = x - floorf(x);
    float yf = y - floorf(y);

    float u = Fade(xf);
    float v = Fade(yf);

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
    float scale = 0.04f; // Controls how "zoomed in" the continents are

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
*/

// =============================================================================
// FILE 2: map_gen_fixed.c
// Same as above but with Fade renamed to FadeNoise to avoid conflict with
// raylib's built-in Fade(Color, float) function. Use this if FILE 1 won't
// compile due to the naming collision.
// Compile: gcc map_gen_fixed.c -o map_gen_fixed -lraylib -lm -lpthread -ldl
// Run:     ./map_gen_fixed     (press SPACE to generate a new world)
// =============================================================================

/*
#include "raylib.h"
#include <stdlib.h>
#include <math.h>

#define WIDTH 800
#define HEIGHT 400
#define GRID_SIZE 4

float Hash(int x, int y, int seed) {
    int n = x + y * 57 + seed * 131;
    n = (n << 13) ^ n;
    return (1.0f - ((n * (n * n * 15731 + 789221) + 1376312589) & 0x7fffffff) / 1073741824.0f);
}

float Lerp(float a, float b, float t) { return a + t * (b - a); }
float FadeNoise(float t) { return t * t * t * (t * (t * 6 - 15) + 10); }

float SmoothNoise2D(float x, float y, int seed) {
    int X = (int)floorf(x);
    int Y = (int)floorf(y);
    float xf = x - floorf(x);
    float yf = y - floorf(y);

    float u = FadeNoise(xf);
    float v = FadeNoise(yf);

    float n00 = (Hash(X, Y, seed) + 1.0f) * 0.5f;
    float n10 = (Hash(X + 1, Y, seed) + 1.0f) * 0.5f;
    float n01 = (Hash(X, Y + 1, seed) + 1.0f) * 0.5f;
    float n11 = (Hash(X + 1, Y + 1, seed) + 1.0f) * 0.5f;

    float x1 = Lerp(n00, n10, u);
    float x2 = Lerp(n01, n11, u);

    return Lerp(x1, x2, v);
}

void DrawWorld(int seed) {
    float scale = 0.04f;

    for (int y = 0; y < HEIGHT; y += GRID_SIZE) {
        for (int x = 0; x < WIDTH; x += GRID_SIZE) {
            float n = SmoothNoise2D(x * scale, y * scale, seed) * 0.7f +
                      SmoothNoise2D(x * scale * 2, y * scale * 2, seed) * 0.3f;

            Color tileColor;
            bool isLand = false;

            if (n < 0.42f) {
                tileColor = (Color){ 75, 85, 135, 255 };
            } else if (n < 0.48f) {
                tileColor = (Color){ 210, 190, 140, 255 };
                isLand = true;
            } else if (n < 0.62f) {
                tileColor = (Color){ 145, 185, 110, 255 };
                isLand = true;
            } else {
                tileColor = (Color){ 80, 135, 85, 255 };
                isLand = true;
            }

            DrawRectangle(x, y, GRID_SIZE, GRID_SIZE, tileColor);

            if (isLand) {
                unsigned int dotHash = (x * 739221 + y * 1376312589 + seed) % 100;
                if (dotHash < 5)
                    DrawRectangle(x + GRID_SIZE/2, y + GRID_SIZE/2, 1, 1, (Color){ 20, 25, 20, 255 });
            }
        }
    }
}

int main(void) {
    InitWindow(WIDTH, HEIGHT, "Procedural 2D Map Generator");
    SetTargetFPS(60);

    int currentSeed = 42;

    while (!WindowShouldClose()) {
        if (IsKeyPressed(KEY_SPACE))
            currentSeed = GetRandomValue(0, 100000);

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
*/

// =============================================================================
// FILE 3: map_gen_image.c  (ACTIVE — compile and run this one headlessly)
// Renders the map directly to a PNG file without opening a window.
// Useful for servers / headless environments.
// Compile: gcc map_gen_image.c -o map_gen_image -lraylib -lm -lpthread -ldl
// Run:     ./map_gen_image [seed]     e.g.  ./map_gen_image 42
// Output:  map_output.png
// =============================================================================

#include "raylib.h"
#include <stdlib.h>
#include <math.h>
#include <stdio.h>

#define WIDTH 800
#define HEIGHT 400
#define GRID_SIZE 4

float Hash(int x, int y, int seed) {
    int n = x + y * 57 + seed * 131;
    n = (n << 13) ^ n;
    return (1.0f - ((n * (n * n * 15731 + 789221) + 1376312589) & 0x7fffffff) / 1073741824.0f);
}

float Lerp(float a, float b, float t) { return a + t * (b - a); }
float FadeNoise(float t) { return t * t * t * (t * (t * 6 - 15) + 10); }

float SmoothNoise2D(float x, float y, int seed) {
    int X = (int)floorf(x);
    int Y = (int)floorf(y);
    float xf = x - floorf(x);
    float yf = y - floorf(y);

    float u = FadeNoise(xf);
    float v = FadeNoise(yf);

    float n00 = (Hash(X, Y, seed) + 1.0f) * 0.5f;
    float n10 = (Hash(X + 1, Y, seed) + 1.0f) * 0.5f;
    float n01 = (Hash(X, Y + 1, seed) + 1.0f) * 0.5f;
    float n11 = (Hash(X + 1, Y + 1, seed) + 1.0f) * 0.5f;

    float x1 = Lerp(n00, n10, u);
    float x2 = Lerp(n01, n11, u);

    return Lerp(x1, x2, v);
}

void DrawWorld(Image *img, int seed) {
    float scale = 0.04f;

    for (int y = 0; y < HEIGHT; y += GRID_SIZE) {
        for (int x = 0; x < WIDTH; x += GRID_SIZE) {
            float n = SmoothNoise2D(x * scale, y * scale, seed) * 0.7f +
                      SmoothNoise2D(x * scale * 2, y * scale * 2, seed) * 0.3f;

            Color tileColor;
            int isLand = 0;

            if (n < 0.42f) {
                tileColor = (Color){ 75, 85, 135, 255 };   // Muted Navy Water
            } else if (n < 0.48f) {
                tileColor = (Color){ 210, 190, 140, 255 };  // Sandy Coast
                isLand = 1;
            } else if (n < 0.62f) {
                tileColor = (Color){ 145, 185, 110, 255 };  // Light Meadow Green
                isLand = 1;
            } else {
                tileColor = (Color){ 80, 135, 85, 255 };    // Forest Green
                isLand = 1;
            }

            // Fill grid cell
            for (int dy = 0; dy < GRID_SIZE && (y + dy) < HEIGHT; dy++)
                for (int dx = 0; dx < GRID_SIZE && (x + dx) < WIDTH; dx++)
                    ImageDrawPixel(img, x + dx, y + dy, tileColor);

            // Scatter black dots on land
            if (isLand) {
                unsigned int dotHash = (x * 739221 + y * 1376312589 + seed) % 100;
                if (dotHash < 5)
                    ImageDrawPixel(img, x + GRID_SIZE/2, y + GRID_SIZE/2, (Color){ 20, 25, 20, 255 });
            }
        }
    }
}

int main(int argc, char *argv[]) {
    int seed = (argc > 1) ? atoi(argv[1]) : 42;

    Image img = GenImageColor(WIDTH, HEIGHT, BLACK);
    DrawWorld(&img, seed);
    ExportImage(img, "map_output.png");
    UnloadImage(img);

    printf("Map saved to map_output.png (seed=%d)\n", seed);
    return 0;
}

