package com.example.streamlit_integration.service;

import com.example.streamlit_integration.entity.Product;
import com.example.streamlit_integration.repository.ProductRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ProductService {

    @Autowired
    private ProductRepository productRepository;

    public List<Product> getSimilarProducts(String certNum) {
        return productRepository.findByCertificationNumber(certNum);
    }

    // 새로운 V/A 기반 제품 검색 로직
    public List<Product> getSimilarProductsByVA(double voltage, double current) {
        // 전압과 전류 값으로 제품을 검색하는 로직
        return productRepository.findByVoltageAndCurrent(voltage, current);
    }
}
