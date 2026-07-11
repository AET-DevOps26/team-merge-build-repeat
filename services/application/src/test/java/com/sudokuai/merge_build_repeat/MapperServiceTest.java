package com.sudokuai.merge_build_repeat;

import com.sudokuai.merge_build_repeat.service.MapperService;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class MapperServiceTest {

    private final MapperService mapperService = new MapperService();

    @Nested
    class MapToListHappyPath {

        @Test
        void shouldMapValid81DigitStringInto9x9Grid() {
            // A completely filled board with valid Sudoku strings or matching characters
            // Let's create a predictable pattern: 9 rows of "123456789"
            String validBoard = "123456789".repeat(9);

            List<List<Integer>> grid = mapperService.mapToList(validBoard);

            assertNotNull(grid);
            assertEquals(9, grid.size(), "Grid must have exactly 9 rows");

            for (int i = 0; i < 9; i++) {
                List<Integer> row = grid.get(i);
                assertEquals(9, row.size(), "Each row must have exactly 9 columns");

                // Assert sequence matches the split index
                assertEquals(1, row.get(0));
                assertEquals(2, row.get(1));
                assertEquals(5, row.get(4));
                assertEquals(9, row.get(8));
            }
        }

        @Test
        void shouldHandleTrimAndMapSuccessfully() {
            // Valid 81 characters surrounded by leading/trailing whitespaces
            String validWithWhitespace = "   " + "0".repeat(81) + "  \n ";

            List<List<Integer>> grid = mapperService.mapToList(validWithWhitespace);

            assertNotNull(grid);
            assertEquals(9, grid.size());
            assertEquals(0, grid.get(0).get(0));
            assertEquals(0, grid.get(8).get(8));
        }
    }

    @Nested
    class MapToListEdgeCasesAndExceptions {

        @Test
        void shouldThrowExceptionWhenInputIsNull() {
            IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, () ->
                    mapperService.mapToList(null)
            );

            assertEquals("Input cannot be null", exception.getMessage());
        }

        @ParameterizedTest
        @ValueSource(strings = {
                "",                                                                             // Empty string
                "123456789",                                                                    // Too short (9 chars)
                "00000000000000000000000000000000000000000000000000000000000000000000000000000000", // Too short (80 chars)
                "0000000000000000000000000000000000000000000000000000000000000000000000000000000000" // Too long (82 chars)
        })
        void shouldThrowExceptionWhenLengthIsNotExactly81Characters(String invalidLengthInput) {
            IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, () ->
                    mapperService.mapToList(invalidLengthInput)
            );

            assertEquals("Input must be exactly 81 characters long", exception.getMessage());
        }

        @ParameterizedTest
        @ValueSource(strings = {
                "12345678a123456789123456789123456789123456789123456789123456789123456789123456789", // Contains lowercase letter
                "12345678912345678912345678912345678912345678912345678912345678912345678912345678X", // Contains uppercase letter
                "0000000000000000000000000000000000000-0000000000000000000000000000000000000000000", // Contains symbol (-)
                "0000000000000000000000000000000000000 0000000000000000000000000000000000000000000"  // Contains inline space
        })
        void shouldThrowExceptionWhenInputContainsNonDigitCharacters(String nonDigitInput) {
            IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, () ->
                    mapperService.mapToList(nonDigitInput)
            );

            assertEquals("Input must contain digits only", exception.getMessage());
        }
    }
}
