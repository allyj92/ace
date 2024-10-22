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
}
