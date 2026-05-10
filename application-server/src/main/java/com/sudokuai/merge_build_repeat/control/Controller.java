package com.sudokuai.merge_build_repeat.control;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;


@RestController
public class Controller {
    @GetMapping(value = "/hello", produces = "text/plain")
    public String helloEndpoint() {
        return "Hello World!";
    }
}
