package com.sudokuai.merge_build_repeat.service;

import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class MapperService {

    public List<List<Integer>> mapToList(String data) {
        if (data == null) {
            throw new IllegalArgumentException("Input cannot be null");
        }

        String normalized = data.trim();
        if (normalized.length() != 81) {
            throw new IllegalArgumentException("Input must be exactly 81 characters long");
        }

        List<List<Integer>> grid = new java.util.ArrayList<>(9);

        for (int row = 0; row < 9; row++) {
            List<Integer> rowList = new java.util.ArrayList<>(9);
            for (int col = 0; col < 9; col++) {
                char ch = normalized.charAt(row * 9 + col);
                if (ch < '0' || ch > '9') {
                    throw new IllegalArgumentException("Input must contain digits only");
                }
                rowList.add(ch - '0');
            }
            grid.add(rowList);
        }

        return grid;
    }

    public String mapToString(List<List<Integer>> grid) {
        if (grid == null) {
            throw new IllegalArgumentException("Grid cannot be null");
        }

        if (grid.size() != 9) {
            throw new IllegalArgumentException("Grid must have exactly 9 rows");
        }

        StringBuilder sb = new StringBuilder(81);

        for (int row = 0; row < 9; row++) {
            List<Integer> rowList = grid.get(row);
            if (rowList == null || rowList.size() != 9) {
                throw new IllegalArgumentException("Each row must have exactly 9 columns");
            }
            for (int col = 0; col < 9; col++) {
                Integer value = rowList.get(col);
                if (value == null) {
                    value = 0;
                }
                if (value < 0 || value > 9) {
                    throw new IllegalArgumentException("Grid values must be between 0 and 9");
                }
                sb.append(value);
            }
        }

        return sb.toString();
    }
}
