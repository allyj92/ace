package com.example.streamlit_integration.repository;

import com.example.streamlit_integration.entity.Product;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ProductDocumentRepository extends JpaRepository<Product,Integer> {
    // 기본적인 CRUD 메서드 제공
}
