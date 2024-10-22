package com.example.streamlit_integration.controller;

import com.example.streamlit_integration.entity.Product;
import com.example.streamlit_integration.service.ProductService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@CrossOrigin(origins = "http://localhost:8501")
@RestController
@RequestMapping("/products")
public class ProductController {

    @Autowired
    private ProductService productService;

    @GetMapping("/similar")
    public ResponseEntity<List<Product>> getSimilarProducts(@RequestParam String certNum) {
        // 디버깅: certNum 값 확인
        System.out.println("Received certification number: " + certNum);

        List<Product> products = productService.getSimilarProducts(certNum);

        // 디버깅: 검색된 제품 리스트 확인
        if (products.isEmpty()) {
            System.out.println("No similar products found for certNum: " + certNum);
        } else {
            System.out.println("Found " + products.size() + " similar products");
            for (Product product : products) {
                System.out.println("Product: " + product.getModelName() + ", Voltage: " + product.getVoltage());
            }
        }

        return ResponseEntity.ok(products);
    }

    // V/A 값을 기반으로 유사한 제품을 찾는 엔드포인트 추가
    @GetMapping("/similar_by_va")
    public ResponseEntity<List<Product>> getSimilarProductsByVA(@RequestParam double voltage, @RequestParam double current) {
        List<Product> products = productService.getSimilarProductsByVA(voltage, current);
        return ResponseEntity.ok(products);


    }




}
