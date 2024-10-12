package com.example.streamlit_integration.repository;

import com.example.streamlit_integration.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;

public interface UserRepository extends JpaRepository<User, Long> {
    // 사용자 아이디(Username)를 통해 User 엔티티를 조회하는 메서드
    User findByUsername(String username);
}
