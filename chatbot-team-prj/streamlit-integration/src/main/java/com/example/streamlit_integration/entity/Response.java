package com.example.streamlit_integration.entity;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;
import java.time.LocalDateTime;

@Getter
@Setter
@Entity
public class Response {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne
    @JoinColumn(name = "user_id")
    private User user;  // 답변을 작성한 사용자

    @OneToOne
    @JoinColumn(name = "question_id", nullable = false)
    private Question question;  // 답변이 연관된 질문 (일대일 관계)


    @Column(nullable = false)
    private String content;  // 답변 내용

    // Other fields and relationships
}


