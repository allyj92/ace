package com.example.streamlit_integration.controller;

import com.example.streamlit_integration.dto.UserDto;
import com.example.streamlit_integration.dto.WishlistRequest;
import com.example.streamlit_integration.entity.Product;
import com.example.streamlit_integration.entity.User;
import com.example.streamlit_integration.entity.WishlistItem;
import com.example.streamlit_integration.repository.UserRepository;
import com.example.streamlit_integration.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/user")
public class UserController {

    @Autowired
    UserRepository userRepository;
    @Autowired
    private UserService userService;

    // 사용자 정보 업데이트 API
    // 사용자 정보 업데이트 API
    public boolean updateUser(UserDto userDto) {
        Optional<User> userOptional = userRepository.findByUsername(userDto.getUsername());

        if (userOptional.isPresent()) {
            User user = userOptional.get();

            // Only update fields that are non-null
            if (userDto.getEmail() != null) {
                user.setEmail(userDto.getEmail());
            }
            if (userDto.getPhoneNumber() != null) {
                user.setPhoneNumber(userDto.getPhoneNumber());
            }

            // Save the updated user back to the database
            userRepository.save(user);
            return true;
        } else {
            System.out.println("User not found: " + userDto.getUsername());
            return false;
        }
    }

    // 사용자 정보 조회 API (username으로 조회)
    @GetMapping("/{username}")
    public ResponseEntity<Map<String, Object>> getUserByUsername(@PathVariable String username) {
        Optional<User> userOptional = userService.findUserByUsername(username);
        if (userOptional.isPresent()) {
            User user = userOptional.get();
            Map<String, Object> userInfo = new HashMap<>();
            userInfo.put("username", user.getUsername());
            userInfo.put("email", user.getEmail());
            userInfo.put("phone_number", user.getPhoneNumber());
            userInfo.put("wishlist", user.getWishlist());

            // Content-Type 명시적으로 설정
            return ResponseEntity
                    .ok()
                    .contentType(MediaType.APPLICATION_JSON)
                    .body(userInfo);
        } else {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(null);
        }
    }

    // 찜 리스트 저장 API
    @PostMapping("/wishlist")
    public ResponseEntity<?> saveWishlist(@RequestBody WishlistRequest request) {
        boolean success = userService.saveWishlist(request.getUsername(), request.getWishlist());
        if (success) {
            return ResponseEntity.ok("찜 리스트가 저장되었습니다.");
        } else {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("찜 리스트 저장 실패");
        }
    }

    // 유저의 찜 리스트 불러오기 API
    @GetMapping("/{username}/wishlist")
    public ResponseEntity<List<Product>> getWishlist(@PathVariable String username) {
        List<WishlistItem> wishlistItems = userService.getWishlist(username);  // WishlistItem 리스트를 가져옴
        if (wishlistItems != null) {
            // WishlistItem에서 Product만 추출하여 List<Product>로 변환
            List<Product> products = wishlistItems.stream()
                    .map(WishlistItem::getProduct)  // WishlistItem에서 Product를 추출
                    .collect(Collectors.toList());

            return ResponseEntity.ok(products);
        } else {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(null);
        }
    }

    // 사용자 정보 부분 업데이트 API (PATCH)
    @PatchMapping("/{username}")
    public ResponseEntity<String> updateUserPartial(@PathVariable String username, @RequestBody UserDto userDto) {
        // 디버깅용 로그 출력
        System.out.println("Patching user: " + username + " with email: " + userDto.getEmail() + " and phone: " + userDto.getPhoneNumber());

        boolean isUpdated = userService.updateUser(userDto);

        if (isUpdated) {
            return ResponseEntity.ok("User partially updated successfully");
        } else {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("Failed to update user partially");
        }
    }





}
