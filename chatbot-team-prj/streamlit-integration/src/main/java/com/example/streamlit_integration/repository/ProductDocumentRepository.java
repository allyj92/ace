package com.example.streamlit_integration.repository;

import com.example.streamlit_integration.entity.ProductDocument;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ProductDocumentRepository extends JpaRepository<ProductDocument,Integer> {
    // 기본적인 CRUD 메서드 제공
}
