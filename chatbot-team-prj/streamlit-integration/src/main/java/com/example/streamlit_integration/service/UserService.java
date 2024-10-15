package com.example.streamlit_integration.service;

import com.example.streamlit_integration.dto.LoginDto;
import com.example.streamlit_integration.dto.UserDto;
import com.example.streamlit_integration.entity.Product;
import com.example.streamlit_integration.entity.User;
import com.example.streamlit_integration.entity.WishlistItem;
import com.example.streamlit_integration.repository.UserRepository;
import com.example.streamlit_integration.repository.WishlistItemRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service  // 이 클래스가 서비스 계층임을 나타내는 어노테이션
public class UserService {

    @Autowired  // 의존성 주입으로 UserRepository를 자동으로 연결
    private UserRepository userRepository;

    @Autowired
    private WishlistItemRepository wishlistItemRepository;

    /*************************     로그인 부분       **************************/
    // 로그인 처리 메서드
    public boolean authenticateUser(LoginDto loginDto) {
        String username = loginDto.getUsername();  // 로그인 요청에서 받은 사용자명
        String password = loginDto.getPassword();  // 로그인 요청에서 받은 비밀번호

        // 사용자명으로 사용자 조회
        Optional<User> userOptional = userRepository.findByUsername(username);

        // 사용자가 존재하고 비밀번호가 일치하는지 확인
        if (userOptional.isPresent()) {
            User user = userOptional.get();  // 조회된 사용자 정보 가져오기
            return user.getPassword().equals(password);  // 비밀번호 일치 여부 확인 (실제 환경에서는 암호화가 필요)
        }

        return false;  // 사용자가 없거나 비밀번호가 틀린 경우 로그인 실패
    }

    /*************************     회원가입 부분       **************************/
    // 회원가입 처리 메서드
    public boolean registerUser(UserDto userDto) {
        // 사용자명이 중복되는지 확인
        Optional<User> existingUser = userRepository.findByUsername(userDto.getUsername());

        // 이미 존재하는 사용자가 있을 경우 회원가입 실패
        if (existingUser.isPresent()) {
            System.out.println("이미 존재하는 사용자명: " + userDto.getUsername());
            return false;  // 중복 사용자
        }

        // UserDto 객체를 User 엔티티로 변환
        User newUser = new User();
        newUser.setUsername(userDto.getUsername());
        newUser.setPassword(userDto.getPassword());
        newUser.setName(userDto.getName());  // name 필드 설정
        newUser.setEmail(userDto.getEmail());
        newUser.setAddress(userDto.getAddress());  // address 필드 설정
        newUser.setPhoneNumber(userDto.getPhoneNumber());  // 전화번호 설정

        // 새로운 사용자 정보를 DB에 저장
        try {
            userRepository.save(newUser);  // 저장 처리
            System.out.println("회원가입 성공: " + userDto.getUsername());
            return true;  // 성공적으로 저장된 경우 true 반환
        } catch (Exception e) {
            System.out.println("회원가입 중 오류 발생: " + e.getMessage());
            return false;  // 저장 중 오류 발생 시 false 반환
        }
    }

    // 찜 리스트 저장 로직
    public boolean saveWishlist(String username, List<Product> wishlistProducts) {
        Optional<User> userOpt = userRepository.findByUsername(username);
        if (userOpt.isPresent()) {
            User user = userOpt.get();
            for (Product product : wishlistProducts) {
                WishlistItem wishlistItem = new WishlistItem();
                wishlistItem.setUser(user);
                wishlistItem.setProduct(product);
                wishlistItemRepository.save(wishlistItem);  // 찜 항목을 저장
            }
            return true;
        }
        return false;
    }

    // 찜 리스트 불러오기 로직
    public List<WishlistItem> getWishlist(String username) {
        Optional<User> userOpt = userRepository.findByUsername(username);  // findByUsername으로 사용자 검색
        if (userOpt.isPresent()) {
            User user = userOpt.get();  // Optional에서 User 객체 가져오기
            return wishlistItemRepository.findByUser(user);  // User 객체를 전달하여 사용자별 찜 리스트 반환
        }
        return null;
    }

    /*************************     Read 부분       **************************/
    // 사용자명으로 사용자 조회
    public Optional<User> findUserByUsername(String username) {
        return userRepository.findByUsername(username);  // 사용자명을 이용해 DB에서 사용자 조회
    }

    // 모든 사용자 조회
    public List<User> findAllUsers() {
        return userRepository.findAll();  // DB에서 모든 사용자 조회
    }

    /*************************     Update 부분       **************************/
    // 사용자 정보 업데이트
    public boolean updateUser(UserDto userDto) {
        // 사용자명으로 사용자 정보 조회
        Optional<User> userOpt = userRepository.findByUsername(userDto.getUsername());

        // 사용자가 존재하는 경우 정보 업데이트
        if (userOpt.isPresent()) {
            User user = userOpt.get();  // 기존 사용자 정보 가져오기
            user.setEmail(userDto.getEmail());  // 이메일 업데이트
            user.setPhoneNumber(userDto.getPhoneNumber());  // 전화번호 업데이트

            userRepository.save(user);  // 수정된 사용자 정보 DB에 저장
            return true;  // 업데이트 성공 시 true 반환
        }
        return false;  // 사용자가 없으면 업데이트 실패
    }

    /*************************     Delete 부분       **************************/
    // 사용자 삭제
    public boolean deleteUserByUsername(String username) {
        // 사용자명으로 사용자 조회
        Optional<User> userOpt = userRepository.findByUsername(username);

        // 사용자가 존재하는 경우 삭제
        if (userOpt.isPresent()) {
            userRepository.delete(userOpt.get());  // 사용자 삭제
            return true;  // 삭제 성공 시 true 반환
        }
        return false;  // 사용자가 없으면 삭제 실패
    }
}
