package com.example.streamlit_integration.repository;

import com.example.streamlit_integration.entity.Product;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface ProductRepository extends JpaRepository<Product,Integer> {
    // 예시: 인증번호로 제품 검색하는 메서드
    List<Product> findByCertificationNumber(String certificationNumber);

    // V/A 값을 기준으로 제품을 검색하는 쿼리 추가
    List<Product> findByVoltageAndCurrent(double voltage, double current);
}
