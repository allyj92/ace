package com.example.streamlit_integration.service;

import com.example.streamlit_integration.dto.LoginDto;
import com.example.streamlit_integration.entity.User;
import com.example.streamlit_integration.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.Optional;

@Service
public class UserService {

    // Inject the UserRepository to access user data
    @Autowired
    private UserRepository userRepository;

    // Method to authenticate user
    public boolean authenticateUser(LoginDto loginDto) {
        String username = loginDto.getUsername();
        String password = loginDto.getPassword();

        // Fetch user by username from the repository
        Optional<User> userOptional = userRepository.findByUsername(username);

        // Check if user exists and the password matches
        if (userOptional.isPresent()) {
            User user = userOptional.get();
            return user.getPassword().equals(password); // Simple password check, consider using encryption in production
        }

        return false; // Return false if user not found or password doesn't match
    }

    public boolean registerUser(User user) {
        // Check if the username already exists
        if (userRepository.findByUsername(user.getUsername()).isPresent()) {
            return false;  // Username already exists, registration fails
        }

        // Save the new user to the database
        userRepository.save(user);
        return true;
    }

    public boolean authenticateUser(String username, String password) {
        Optional<User> userOptional = userRepository.findByUsername(username);
        if (userOptional.isPresent()) {
            User user = userOptional.get();
            return user.getPassword().equals(password);  // Assuming plain-text password, use hashing in production
        }
        return false;
    }
}
