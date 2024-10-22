package com.example.streamlit_integration.repository;


import com.example.streamlit_integration.dto.UserDto;
import com.example.streamlit_integration.entity.Product;
import com.example.streamlit_integration.entity.User;
import com.example.streamlit_integration.entity.WishlistItem;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface WishlistRepository extends JpaRepository<WishlistItem, Long> {
    List<WishlistItem> findByUserId(Long userId);
    boolean existsByUserAndProduct(User user, Product product);
    void deleteByUserIdAndProductId(Long userId, Integer productId);
    void deleteByUserId(Long userId);

    // 사용자 기반으로 찜한 상품 목록 조회
    List<WishlistItem> findByUser(User user);

    // 사용자 기반으로 찜한 상품 전체 삭제
    void deleteAllByUser(User user);
}
