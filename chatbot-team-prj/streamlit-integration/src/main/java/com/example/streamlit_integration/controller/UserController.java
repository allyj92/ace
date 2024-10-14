package com.example.streamlit_integration.controller;

import com.example.streamlit_integration.dto.UserDto;
import com.example.streamlit_integration.entity.User;
import com.example.streamlit_integration.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

@RestController
@RequestMapping("/user")
public class UserController {

    @Autowired
    private UserService userService;

    // 사용자 정보 업데이트 API
    @PutMapping("/update")
    public ResponseEntity<String> updateUser(@RequestBody UserDto userDto) {
        boolean isUpdated = userService.updateUser(userDto);

        if (isUpdated) {
            return ResponseEntity.ok("User updated successfully");
        } else {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("Failed to update user");
        }
    }

    // 사용자 정보 조회 API (username으로 조회)
    @GetMapping("/{username}")
    public ResponseEntity<?> getUserByUsername(@PathVariable String username) {
        Optional<User> userOptional = userService.findUserByUsername(username);  // userRepository 대신 userService로 변경
        if (userOptional.isPresent()) {
            User user = userOptional.get();
            // 필요한 정보를 담아 반환
            Map<String, Object> userInfo = new HashMap<>();
            userInfo.put("username", user.getUsername());
            userInfo.put("email", user.getEmail());
            userInfo.put("phone_number", user.getPhoneNumber());
            userInfo.put("wishlist", user.getWishlist());  // 사용자 찜 목록

            return ResponseEntity.ok(userInfo);
        } else {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body("사용자를 찾을 수 없습니다.");
        }
    }
}
