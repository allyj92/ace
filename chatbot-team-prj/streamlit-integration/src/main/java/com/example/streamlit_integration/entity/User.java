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
@NoArgsConstructor
@AllArgsConstructor
@Entity
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String username;  // 아이디

    @Column(nullable = false)
    private String password;  // 비밀번호

    @Column(nullable = false)
    private String name;      // 이름

    @Column(nullable = false, unique = true)
    private String email;     // 이메일

    @Column(nullable = false)
    private String address;   // 주소

    @Column(nullable = false)
    private String phoneNumber;   // 주소

    @ElementCollection
    private List<String> wishlist;  // 찜 목록

    @Column(updatable = false)
    private LocalDateTime createdDate;  // 생성일

    private LocalDateTime updatedDate;  // 수정일

    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<Question> questions;  // 유저가 작성한 질문 목록

    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<Response> responses;  // 유저가 작성한 답변 목록

    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<WishlistItem> wishlistItems;  // 찜한 상품 목록

    @PrePersist
    protected void onCreate() {
        createdDate = LocalDateTime.now();
    }

    @PreUpdate
    protected void onUpdate() {
        updatedDate = LocalDateTime.now();
    }


}