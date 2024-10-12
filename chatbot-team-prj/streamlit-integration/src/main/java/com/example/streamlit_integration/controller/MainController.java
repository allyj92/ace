package com.example.streamlit_integration.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.servlet.view.RedirectView;

@Controller
public class MainController {

    @GetMapping("/")
    public RedirectView redirectToStreamlit() {
        // "/" 경로로 접근 시 스트림릿 페이지로 리다이렉트
        // "/" 경로로 접근 시 스트림릿 페이지로 리다이렉트
        return new RedirectView("http://localhost:8501");
    }
}