package com.example.streamlit_integration.service;

import com.example.streamlit_integration.dto.LoginDto;
import com.example.streamlit_integration.dto.UserDto;
import com.example.streamlit_integration.entity.User;
import com.example.streamlit_integration.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
public class UserService {

    @Autowired
    private UserRepository userRepository;

    // 로그인 처리 메서드
    public boolean authenticateUser(LoginDto loginDto) {
        String username = loginDto.getUsername();
        String password = loginDto.getPassword();

        // 사용자 조회
        Optional<User> userOptional = userRepository.findByUsername(username);

        // 사용자 존재 여부와 비밀번호 일치 여부 확인
        if (userOptional.isPresent()) {
            User user = userOptional.get();
            return user.getPassword().equals(password);  // 간단한 비밀번호 체크, 실제로는 암호화를 사용해야 함
        }

        return false;
    }

    // 회원가입 처리 메서드
    public boolean registerUser(UserDto userDto) {
        // 중복 사용자 체크
        Optional<User> existingUser = userRepository.findByUsername(userDto.getUsername());

        if (existingUser.isPresent()) {
            System.out.println("이미 존재하는 사용자명: " + userDto.getUsername());
            return false;  // 이미 존재하는 사용자
        } else {
            System.out.println("새로운 사용자명: " + userDto.getUsername());
        }

        // UserDto를 User 엔티티로 변환
        User newUser = new User();
        newUser.setUsername(userDto.getUsername());
        newUser.setPassword(userDto.getPassword());  // 실제로는 비밀번호 암호화를 적용해야 함
        newUser.setEmail(userDto.getEmail());
        newUser.setPhoneNumber(userDto.getPhoneNumber());

        // 새로운 사용자 저장
        try {
            userRepository.save(newUser);
            System.out.println("회원가입 성공: " + userDto.getUsername());
            return true;
        } catch (Exception e) {
            System.out.println("회원가입 중 오류 발생: " + e.getMessage());
            return false;
        }
    }
    }