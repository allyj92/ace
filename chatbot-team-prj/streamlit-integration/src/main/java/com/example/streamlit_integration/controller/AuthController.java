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
@CrossOrigin(origins = "http://localhost:8501")
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

    // 회원가입 처리
    @PostMapping("/signup")
    public ResponseEntity<?> registerUser(@RequestBody UserDto userDto) {
        if (userDto.getUsername() == null || userDto.getPassword() == null || userDto.getName() == null || userDto.getEmail() == null) {
            return ResponseEntity.badRequest().body("필수 정보를 모두 입력해주세요.");
        }

        try {
            boolean isRegistered = userService.registerUser(userDto);
            if (isRegistered) {
                return ResponseEntity.ok("회원가입에 성공했습니다.");
            } else {
                return ResponseEntity.badRequest().body("이미 존재하는 사용자입니다.");
            }
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("회원가입 중 오류가 발생했습니다.");
        }
    }
}
