package com.sudokuai.merge_build_repeat.config;

import com.sudokuai.merge_build_repeat.model.GameTemplate;
import com.sudokuai.merge_build_repeat.repository.GameTemplateRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.Random;

@Component
public class DatabaseInitializer implements CommandLineRunner {

    private final GameTemplateRepository repository;
    private final Random random = new Random();

    // Standard valid Sudoku solution and masked templates (81-character strings)
    private static final String BASE_SOLUTION = "534678912672195348198342567859761423426853791713924856961537284287419635345286179";
    private static final String EASY_TEMPLATE = "530070000600195000098000060800060003400803001700020006060000280000419005000080079";
    private static final String MEDIUM_TEMPLATE = "000600012000000300190042000850060020400803001010020006060000284007419000040080000";
    private static final String HARD_TEMPLATE = "000000012000000300100042000800060020400803001010020000060000200007419000040000000";

    public DatabaseInitializer(GameTemplateRepository repository) {
        this.repository = repository;
    }

    @Override
    public void run(String... args) throws Exception {
        // Prevent duplicate entries if the database already has records
        if (repository.count() == 0) {
            List<String> difficulties = List.of("easy", "medium", "hard");

            for (int i = 0; i < 20; i++) {
                String difficulty = difficulties.get(random.nextInt(difficulties.size()));
                String templateData = getTemplateByDifficulty(difficulty);

                GameTemplate game = new GameTemplate();
                game.setDifficulty(difficulty);
                game.setTemplateData(templateData);
                game.setSolutionData(BASE_SOLUTION);

                repository.save(game);
            }
            System.out.println(">> Database successfully populated with 20 random Sudoku templates.");
        } else {
            System.out.println(">> Database already contains data. Skipping initialization.");
        }
    }

    private String getTemplateByDifficulty(String difficulty) {
        return switch (difficulty) {
            case "easy" -> EASY_TEMPLATE;
            case "medium" -> MEDIUM_TEMPLATE;
            case "hard" -> HARD_TEMPLATE;
            default -> EASY_TEMPLATE;
        };
    }
}
