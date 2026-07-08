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
            throw new IllegalArgumentException("Input must be exactly81 characters long");
        }

        List<List<Integer>> grid = new java.util.ArrayList<>(9);

        for (int row = 0; row < 9; row++) {
            List<Integer> rowList = new java.util.ArrayList<>(9);
            for (int col = 0; col < 9; col++) {
                char ch = normalized.charAt(row * 9 + col);
                if (!Character.isDigit(ch)) {
                    throw new IllegalArgumentException("Input must contain digits only");
                }
                rowList.add(ch - '0');
            }
            grid.add(rowList);
        }

        return grid;
    }
}
