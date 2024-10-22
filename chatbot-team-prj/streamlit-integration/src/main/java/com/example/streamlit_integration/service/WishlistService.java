package com.example.streamlit_integration.service;

import com.example.streamlit_integration.entity.Product;
import com.example.streamlit_integration.entity.User;
import com.example.streamlit_integration.entity.WishlistItem;
import com.example.streamlit_integration.repository.ProductRepository;
import com.example.streamlit_integration.repository.UserRepository;
import com.example.streamlit_integration.repository.WishlistRepository;
import org.springframework.beans.factory.annotation.Autowired;

import javax.persistence.EntityNotFoundException;
import java.time.LocalDateTime;
import java.util.Optional;

public class WishlistService {

    @Autowired
    private WishlistRepository wishlistRepository;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private ProductRepository productRepository;

    public boolean addWishlistItem(String username, int productId) {
        Optional<User> userOpt = userRepository.findByUsername(username);
        if (userOpt.isPresent()) {
            User user = userOpt.get();

            // Product가 존재하는지 확인
            Optional<Product> productOpt = productRepository.findById(productId);
            if (productOpt.isPresent()) {
                Product product = productOpt.get();

                // WishlistItem 생성 및 저장
                WishlistItem wishlistItem = new WishlistItem();
                wishlistItem.setUser(user);
                wishlistItem.setProduct(product);
                wishlistRepository.save(wishlistItem);
                return true;
            } else {
                throw new EntityNotFoundException("Product with id " + productId + " not found.");
            }
        }
        return false;
    }

    // 찜한 상품 저장
    public void addProductToWishlist(Long userId, Integer productId) {
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new RuntimeException("User not found"));

        Product product = productRepository.findById(productId)
                .orElseThrow(() -> new RuntimeException("Product not found"));

        // 이미 찜한 상품인지 확인
        if (wishlistRepository.existsByUserAndProduct(user, product)) {
            throw new RuntimeException("This product is already in the wishlist");
        }

        WishlistItem wishlistItem = new WishlistItem();
        wishlistItem.setUser(user);
        wishlistItem.setProduct(product);
        wishlistItem.setAddedDate(LocalDateTime.now());

        wishlistRepository.save(wishlistItem);
    }

    // 특정 찜한 상품 삭제
    public void removeProductFromWishlist(Long userId, Integer productId) {
        wishlistRepository.deleteByUserIdAndProductId(userId, productId);
    }

    // 모든 찜한 상품 삭제
    public void clearWishlist(Long userId) {
        wishlistRepository.deleteByUserId(userId);
    }
}