package com.example.streamlit_integration.repository;

import com.example.streamlit_integration.entity.Question;
import com.example.streamlit_integration.entity.Response;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;


@Repository
public interface ResponseRepository extends JpaRepository<Response, Long> {
        List<Response> findByQuestion(Question question);  // 특정 질문에 대한 답변들 찾기
}


