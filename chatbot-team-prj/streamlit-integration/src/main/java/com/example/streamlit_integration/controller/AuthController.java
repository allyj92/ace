package com.example.streamlit_integration.controller;

import com.example.streamlit_integration.dto.LoginDto;
import com.example.streamlit_integration.dto.UserDto;
import com.example.streamlit_integration.entity.User;
import com.example.streamlit_integration.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/auth")
@CrossOrigin(origins = "http://numbero.co.kr")
public class AuthController {

    @Autowired
    private UserService userService;

    // 로그인 처리
    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestBody LoginDto loginRequest) {
        boolean isAuthenticated = userService.authenticateUser(loginRequest);  // LoginDto 전체를 전달

        if (isAuthenticated) {
            return ResponseEntity.ok("로그인에 성공했습니다.");
        } else {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("로그인에 실패했습니다.");
        }
    }

    // 회원가입 처리 API
    @PostMapping("/signup")
    public ResponseEntity<String> signup(@RequestBody UserDto userDto) {
        boolean isRegistered = userService.registerUser(userDto);

        if (isRegistered) {
            return ResponseEntity.ok("회원가입 성공!");
        } else {
            return ResponseEntity.badRequest().body("회원가입 실패: 이미 존재하는 사용자명입니다.");
        }
    }
}