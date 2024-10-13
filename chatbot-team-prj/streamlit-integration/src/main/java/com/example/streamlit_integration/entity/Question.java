package com.example.streamlit_integration.entity;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import javax.persistence.*;
import java.time.LocalDateTime;
import java.util.List;

@Getter
@Setter
@Entity
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "questions")  // 테이블 이름 명시
public class Question {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;  // 질문 ID

    @ManyToOne
    @JoinColumn(name = "user_id", nullable = false)
    private User user;  // 질문 작성자

    @ManyToOne
    @JoinColumn(name = "product_id")
    private Product product;  // 질문이 연관된 제품

    @Column(nullable = false)
    private String title;  // 질문 제목

    @Column(nullable = false, columnDefinition = "TEXT")
    private String content;  // 질문 내용

    @OneToOne(mappedBy = "question", cascade = CascadeType.ALL, orphanRemoval = true)
    private Response response;  // 질문에 대한 단일 답변

    @Column(nullable = false, updatable = false)
    private LocalDateTime createdDate;  // 질문 생성일

    private LocalDateTime updatedDate;  // 질문 수정일

    @PrePersist
    protected void onCreate() {
        createdDate = LocalDateTime.now();
    }

    @PreUpdate
    protected void onUpdate() {
        updatedDate = LocalDateTime.now();
    }
}
