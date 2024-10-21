package com.example.streamlit_integration.dto;

import com.example.streamlit_integration.entity.Question;
import lombok.Getter;
import lombok.RequiredArgsConstructor;

import java.time.LocalDateTime;

@Getter
@RequiredArgsConstructor
public class QuestionResponse {

    private Long id;
    private String title;
    private String content;
    private LocalDateTime createdAt;

    public QuestionResponse(Question question){
        this.id = question.getId();
        this.title = question.getTitle();
        this.content = question.getContent();
        this.createdAt = question.getCreatedDate();
    }
}
