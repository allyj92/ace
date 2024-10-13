package com.example.streamlit_integration.entity;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import javax.persistence.*;
import java.time.LocalDateTime;

@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
@Entity
@Table(name = "wishlist_item")  // 테이블 이름을 명시적으로 지정
public class WishlistItem {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne
    @JoinColumn(name = "user_id")
    private User user;  // 찜한 사용자

    @ManyToOne
    @JoinColumn(name = "product_id")
    private Product product;  // 찜한 상품

    // 추가적으로 찜한 날짜를 기록할 수 있음
    @Column(nullable = false)
    private LocalDateTime addedDate;

    @PrePersist
    protected void onCreate() {
        addedDate = LocalDateTime.now();
    }
}