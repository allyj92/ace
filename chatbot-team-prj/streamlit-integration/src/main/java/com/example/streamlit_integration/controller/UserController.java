package com.example.streamlit_integration.controller;

import com.example.streamlit_integration.entity.User;
import com.example.streamlit_integration.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/user")
public class UserController {

    @Autowired
    private UserService userService;

    // 회원가입 요청 처리
    @PostMapping("/signup")
    public ResponseEntity<Map<String, Object>> registerUser(@RequestBody User user) {
        Map<String, Object> response = new HashMap<>();
        try {
            boolean isRegistered = userService.registerUser(user);
            if (isRegistered) {
                response.put("registered", true);
                return ResponseEntity.ok(response);
            } else {
                response.put("error", "이미 존재하는 사용자입니다.");
                return ResponseEntity.badRequest().body(response);
            }
        } catch (IllegalArgumentException e) {
            response.put("error", "잘못된 입력값입니다. 회원가입에 실패했습니다.");
            return ResponseEntity.badRequest().body(response);
        } catch (Exception e) {
            response.put("error", "회원가입 중 오류가 발생했습니다: " + e.getMessage());
            return ResponseEntity.status(500).body(response);
        }
    }

    @GetMapping("/signup")
    public String showSignupForm() {
        return "signup";  // Thymeleaf 템플릿을 사용할 경우, signup.html 파일을 렌더링
    }

    // 로그인 요청 처리
    @PostMapping("/login")
    public ResponseEntity<Map<String, Object>> loginUser(@RequestBody User loginRequest) {
        Map<String, Object> response = new HashMap<>();
        try {
            boolean isAuthenticated = userService.authenticateUser(loginRequest.getUsername(), loginRequest.getPassword());
            if (isAuthenticated) {
                response.put("authenticated", true);
                return ResponseEntity.ok(response);
            } else {
                response.put("error", "잘못된 사용자명 또는 비밀번호입니다.");
                return ResponseEntity.status(401).body(response);
            }
        } catch (IllegalArgumentException e) {
            response.put("error", "잘못된 입력값입니다. 로그인에 실패했습니다.");
            return ResponseEntity.badRequest().body(response);
        } catch (Exception e) {
            response.put("error", "로그인 중 오류가 발생했습니다: " + e.getMessage());
            return ResponseEntity.status(500).body(response);
        }
    }
}
