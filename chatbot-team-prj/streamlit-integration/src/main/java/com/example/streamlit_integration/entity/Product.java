package com.example.streamlit_integration.entity;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;
import java.util.List;

@Getter
@Setter
@Entity
@Table(name = "product")  // 테이블 이름을 명시적으로 지정
public class Product {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)  // IDENTITY 전략 사용
    private Integer id;

    private String certificationNumber;
    private double current;
    @Column(length = 5000)
    private String imageUrl;
    private String modelName;
    private String productName;
    @Column(length = 10000)
    private String productUrl;
    private double voltage;

    @OneToMany(mappedBy = "product", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Question> questions;  // 제품에 대한 질문 리스트

}
