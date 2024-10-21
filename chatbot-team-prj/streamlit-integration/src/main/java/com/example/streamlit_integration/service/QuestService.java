package com.example.streamlit_integration.service;

import com.example.streamlit_integration.dto.QuestionDto;
import com.example.streamlit_integration.dto.QuestionResponse;
import com.example.streamlit_integration.entity.Question;
import com.example.streamlit_integration.entity.User;
import com.example.streamlit_integration.repository.QuestionRepository;
import com.example.streamlit_integration.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.NoSuchElementException;
import java.util.concurrent.RejectedExecutionException;

@Service
@RequiredArgsConstructor
public class QuestService {

    private final QuestionRepository questionRepository;
    private final UserRepository userRepository;


    public void createQuestion(QuestionDto req, Long userId){
        User user = userRepository.findById(userId).orElseThrow(() ->
                new NoSuchElementException("사용자를 찾을 수 없습니다.")
        );
        // user 부분 시큐리티 미완성으로 임시 구현
        Question question = new Question(req, user);
        questionRepository.save(question);
    }

    public QuestionResponse getQuestion(Long userId, Long questionId){
        User user = userRepository.findById(userId).orElseThrow(() ->
                new NoSuchElementException("사용자를 찾을 수 없습니다.")
        );
        // user 부분 시큐리티 미완성으로 임시 구현
        Question question = questionRepository.findById(questionId).orElseThrow(()-> new NoSuchElementException("이 질문은 찾을 수 없습니다."));
        if (!question.getUser().getId().equals(user.getId())){
            throw new RejectedExecutionException("조회할 수 없습니다.");
        }
        return new QuestionResponse(question);
    }

    @Transactional
    public void updateQuestion(QuestionDto req, Long userId, Long questionId){
        User user = userRepository.findById(userId).orElseThrow(() ->
                new NoSuchElementException("사용자를 찾을 수 없습니다.")
        );
        // user 부분 시큐리티 미완성으로 임시 구현
        Question question = questionRepository.findById(questionId).orElseThrow(()-> new NoSuchElementException("이 질문은 찾을 수 없습니다."));
        if (!question.getUser().getId().equals(user.getId())){
            throw new RejectedExecutionException("수정할 수 없습니다.");
        }
        question.update(req);
    }

    @Transactional
    public void deleteQuestion(Long questionId, Long userId){
        User user = userRepository.findById(userId).orElseThrow(() ->
                new NoSuchElementException("사용자를 찾을 수 없습니다.")
        );
        // user 부분 시큐리티 미완성으로 임시 구현
        Question question = questionRepository.findById(questionId).orElseThrow(()-> new NoSuchElementException("이 질문은 찾을 수 없습니다."));
        if (!question.getUser().getId().equals(user.getId())){
            throw new RejectedExecutionException("삭제할 수 없습니다.");
        }
        questionRepository.delete(question);
    }

}
