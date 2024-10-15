package com.example.streamlit_integration.controller;

import com.example.streamlit_integration.dto.UserDto;
import com.example.streamlit_integration.dto.WishlistRequest;
import com.example.streamlit_integration.entity.Product;
import com.example.streamlit_integration.entity.User;
import com.example.streamlit_integration.entity.WishlistItem;
import com.example.streamlit_integration.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
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
    private UserService userService;

    // 사용자 정보 업데이트 API
    // 사용자 정보 업데이트 API
    @PutMapping("/update")
    public ResponseEntity<String> updateUser(@RequestBody UserDto userDto) {
        // 디버깅용 로그 출력
        System.out.println("Updating user: " + userDto.getUsername() + ", " + userDto.getEmail() + ", " + userDto.getPhoneNumber());

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

}
