package com.example.streamlit_integration.dto;

import com.example.streamlit_integration.entity.Product;
import lombok.Getter;
import lombok.Setter;

import java.util.List;

@Getter
@Setter
public class WishlistRequest {
    private String username;
    private List<Product> wishlist;
}
