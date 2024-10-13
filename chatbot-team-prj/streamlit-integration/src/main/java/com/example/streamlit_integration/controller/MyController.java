package com.example.streamlit_integration.controller;

import com.example.streamlit_integration.dto.MyData;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/")
public class MyController {
    @PostMapping("/process-data")
    public ResponseEntity<String> processData(@RequestBody MyData data) {
        String response = "Received: " + data.getField1() + ", " + data.getField2();
        return ResponseEntity.ok(response);
    }
}