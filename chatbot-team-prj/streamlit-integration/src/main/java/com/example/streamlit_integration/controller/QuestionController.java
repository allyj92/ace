package com.example.streamlit_integration.controller;

import com.example.streamlit_integration.dto.QuestionDto;
import com.example.streamlit_integration.dto.QuestionResponse;
import com.example.streamlit_integration.entity.User;
import com.example.streamlit_integration.service.QuestService;
import com.example.streamlit_integration.service.UserService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequiredArgsConstructor
public class QuestionController {

    private final QuestService questService;

    @PostMapping("/question")
    public ResponseEntity<String> createQuestion(
            @RequestBody QuestionDto req,
            @RequestParam Long userId
            // user 부분 시큐리티 미완성으로 임시 구현
    ){
        questService.createQuestion(req, userId);
        return ResponseEntity.status(HttpStatus.CREATED).body("질문 등록");
    }

    @GetMapping("/question/{questionId}")
    public ResponseEntity<QuestionResponse> getQuestion(
            @RequestParam Long userId,
            // user 부분 시큐리티 미완성으로 임시 구현
            @PathVariable(name = "questionId") Long questionId
    ){
        return ResponseEntity.status(HttpStatus.OK).body(questService.getQuestion(userId, questionId));
    }

    @PatchMapping("/question/{questionId}")
    public ResponseEntity<String> updateQuestion(
            @RequestBody QuestionDto req,
            @RequestParam Long userId,
            // user 부분 시큐리티 미완성으로 임시 구현
            @PathVariable(name = "questionId") Long questionId
    ){
        questService.updateQuestion(req, userId, questionId);
        return ResponseEntity.status(HttpStatus.OK).body("질문 수정");
    }

    @DeleteMapping("/question/{questionId}")
    public ResponseEntity<String> deleteQuestion(
            @PathVariable(name = "questionId") Long questionId,
            @RequestParam Long userId
            // user 부분 시큐리티 미완성으로 임시 구현
    ){
        questService.deleteQuestion(questionId, userId);
        return ResponseEntity.status(HttpStatus.NO_CONTENT).body("질문 삭제");
    }
}
