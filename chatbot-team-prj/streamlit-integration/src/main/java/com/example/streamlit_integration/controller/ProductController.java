package com.example.streamlit_integration.controller;

import com.example.streamlit_integration.entity.Product;
import com.example.streamlit_integration.service.ProductService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/products")
public class ProductController {

    @Autowired
    private ProductService productService;

    @GetMapping("/similar")
    public ResponseEntity<List<Product>> getSimilarProducts(@RequestParam String certNum) {
        List<Product> products = productService.getSimilarProducts(certNum);
        return ResponseEntity.ok(products);
    }
}