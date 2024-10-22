package com.example.streamlit_integration.repository;

import com.example.streamlit_integration.entity.Product;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface ProductRepository extends JpaRepository<Product,Integer> {
    // 예시: 인증번호로 제품 검색하는 메서드
    List<Product> findByCertificationNumber(String certificationNumber);
}
