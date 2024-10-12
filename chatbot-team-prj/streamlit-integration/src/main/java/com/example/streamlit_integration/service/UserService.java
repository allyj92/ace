package com.example.streamlit_integration.service;

import com.example.streamlit_integration.entity.User;
import com.example.streamlit_integration.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
public class UserService {

    @Autowired
    private UserRepository userRepository;

    // 회원가입 처리 메서드
    public boolean registerUser(User user) {
        // 사용자명이 이미 존재하는지 확인
        Optional<User> existingUser = Optional.ofNullable(userRepository.findByUsername(user.getUsername()));
        if (existingUser.isPresent()) {
            return false;  // 이미 존재하는 사용자
        }

        // 새 사용자 저장
        userRepository.save(user);
        return true;
    }

    // 사용자 인증 메서드 (로그인)
    public boolean authenticateUser(String username, String password) {
        // 사용자명으로 사용자를 찾음
        Optional<User> user = Optional.ofNullable(userRepository.findByUsername(username));
        // 사용자명 또는 비밀번호 불일치
        // 비밀번호가 일치하는지 확인
        return user.map(value -> value.getPassword().equals(password)).orElse(false);
    }
}