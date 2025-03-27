# reactNativeProject

frontend/
│── src/
│   ├── api/               # API gọi Django & Firebase
│   │   ├── authApi.js     # Đăng nhập/đăng ký
│   │   ├── userApi.js     # API quản lý người dùng
│   │   ├── firebaseAuth.js     # API quản lý Firebase

│
│   ├── components/        # Component dùng chung
│   │   ├── Button/Button.tsx
│   │   ├── Input/Input.tsx
│   │   ├── UserCard/UserCard.tsx
│
│   ├── hooks/             # Custom hooks
│   │   ├── useAuth.js
│
│   ├── navigation/        # Điều hướng trong ứng dụng
│   │   ├── AppNavigator.js
│   │   ├── AuthNavigator.js
│
│   ├── redux/             # Redux Toolkit
│   │   ├── store.js
│   │   ├── slices/
│   │   │   ├── authSlice.js
│   │   │   ├── userSlice.js
│
│   ├── screens/           # Các màn hình chính
│   │   ├── LoginScreen.tsx
│   │   ├── HomeScreen.tsx
│   │   ├── ProfileScreen.tsx
│
│   ├── utils/             # Helper functions
│   │   ├── validate.js
│
│   ├── App.tsx             # Component chính
│   ├── firebase.js        # Cấu hình Firebase
│   ├── styles.js          # Styles chung
│
│── package.json           # Các thư viện React Native
│── .env                   # Biến môi trường
│── index.js               # Entry point


# B1: build basic frame
# - tạo New repository
# - clone dự án 
# - tạo file .gitignore, README.md
# - khởi tạo git : git init
# - khởi tạo package.json : npm init
# - tải nodemon : npm install -g nodemon


# B2: build backend 
# - tạo thư mục backend : mkdir backend
# - cd backend
# - # Tạo virtual environment môi trường ảo : python -m venv venv  

# -  Kích hoạt môi trường ảo:
# --- Nếu dùng (Mac/Linux) : source venv/bin/activate 
# --- Nếu dùng Windows, chạy: venv\Scripts\activate

# cài đặt django 
# - pip install django djangorestframework django-cors-headers djangorestframework-simplejwt

# - Tạo Django project: django-admin startproject config
# - Cấu hình Django trong config/settings.py
# bổ sung config/settings.py
INSTALLED_APPS = [
    # bổ sung
    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt',
]

MIDDLEWARE = [
    # bổ sung
    'corsheaders.middleware.CorsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# - Cấu hình CORS : CORS_ALLOW_ALL_ORIGINS = True  Cho phép mọi frontend kết nối

# -  Tạo ứng dụng API : python manage.py startapp api
# - Thêm api vào INSTALLED_APPS trong settings.py.
INSTALLED_APPS = [
     # Ứng dụng
    'api',
]
# Tạo Model trong api/models.py : 
# touch api/models.py (Linux/macOS) hoặc New-Item api/models.py -ItemType "file"

from django.db import models

class UserProfile(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

# - Chạy migration
# python manage.py makemigrations
# python manage.py migrate


# - Tạo API Endpoint trong api/views.py 
# touch api/views.py  (Linux/macOS) hoặc New-Item api/views.py  -ItemType "file"

from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import UserProfile

@api_view(['GET'])
def get_users(request):
    users = UserProfile.objects.all().values('id', 'username', 'email')
    return Response(users)

# - Tạo API Endpoint trong api/urls.py
# touch api/urls.py  (Linux/macOS) hoặc New-Item api/urls.py  -ItemType "file"

from django.urls import path
from .views import get_users

urlpatterns = [
    path('users/', get_users),
]

# - Cấu hình config/urls.py
from django.urls import path, include

urlpatterns = [
    path('api/', include('api.urls')),
]

# - Chạy server : python manage.py runserver

# -----------------------------------------------------

# B3: Cài đặt Frontend (React Native + Redux)
# - cd .. về thư mục gốc
# - npx @react-native-community/cli init frontend
# - cd frontend
# - npm install react-redux @reduxjs/toolkit axios react-navigation 

# - npm install @react-navigation/native
# - npm install @react-navigation/stack
# - npm install react-native-screens react-native-safe-area-context
# - npm install react-native-gesture-handler react-native-reanimated

# ---- tạo  src/redux/store.js -----
import { configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
  },
});

# ---- Tạo src/redux/slices/authSlice.js
import { createSlice } from '@reduxjs/toolkit';

const authSlice = createSlice({
  name: 'auth',
  initialState: { user: null, token: null },
  reducers: {
    login: (state, action) => {
      state.user = action.payload.user;
      state.token = action.payload.token;
    },
    logout: (state) => {
      state.user = null;
      state.token = null;
    },
  },
});

export const { login, logout } = authSlice.actions;
export default authSlice.reducer;

# - Kết nối Redux trong App.js
import React from 'react';
import { Provider } from 'react-redux';
import { store } from './src/redux/store';
import HomeScreen from './src/screens/HomeScreen';

export default function App() {
  return (
    <Provider store={store}>
      <HomeScreen />
    </Provider>
  );
}

# - Tạo src/api/authApi.js
import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api';

export const fetchUsers = async () => {
  try {
    const response = await axios.get(`${API_URL}/users/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching users:', error);
  }
};
# - Gọi API trong HomeScreen.js
# - tạo src/HomeScreen.js
import React, { useEffect, useState } from 'react';
import { View, Text } from 'react-native';
import { fetchUsers } from '../api/authApi';

const HomeScreen = () => {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    fetchUsers().then(setUsers);
  }, []);

  return (
    <View>
      {users.map((user) => (
        <Text key={user.id}>{user.username} - {user.email}</Text>
      ))}
    </View>
  );
};

export default HomeScreen;


# Kết nối Firebase Authentication : npm install firebase
# tạo src/firebase.js
import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';

const firebaseConfig = {
  apiKey: "your_api_key",
  authDomain: "your_project.firebaseapp.com",
  projectId: "your_project_id",
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);

# tạo src/api/firebaseAuth.js

import { auth } from '../firebase';
import { signInWithEmailAndPassword } from 'firebase/auth';

export const loginWithFirebase = async (email, password) => {
  try {
    const userCredential = await signInWithEmailAndPassword(auth, email, password);
    return userCredential.user;
  } catch (error) {
    console.error(error.message);
    return null;
  }
};

# - Gọi Firebase trong LoginScreen.js
import React, { useState } from 'react';
import { View, TextInput, Button, Text } from 'react-native';
import { loginWithFirebase } from '../api/firebaseAuth';

const LoginScreen = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async () => {
    const user = await loginWithFirebase(email, password);
    if (user) console.log('Login successful:', user);
    else console.log('Login failed');
  };

  return (
    <View>
      <TextInput placeholder="Email" onChangeText={setEmail} />
      <TextInput placeholder="Password" onChangeText={setPassword} secureTextEntry />
      <Button title="Login" onPress={handleLogin} />
    </View>
  );
};

# cài đặt bổ sung : npm install --save-dev @babel/core @babel/preset-env @babel/preset-react babel-eslint
# npm install --save-dev @babel/eslint-parser
# npm install --save-dev eslint-plugin-react
# babel.config.js
module.exports = {
  presets: [
    'module:@react-native/babel-preset',
    '@babel/preset-env',
    '@babel/preset-react'
  ],

};

1️⃣ Khởi động Backend (Django)
Mở terminal/cmd, điều hướng vào thư mục backend và chạy:

sh
Sao chép
Chỉnh sửa
source venv/bin/activate  # Kích hoạt môi trường ảo (Mac/Linux)
# Nếu dùng Windows:
# venv\Scripts\activate

python manage.py runserver  # Chạy server Django
✅ Django API sẽ chạy tại: http://127.0.0.1:8000/api/

2️⃣ Khởi động Frontend (React Native)
Mở terminal/cmd, điều hướng vào thư mục frontend và chạy:

npx react-native start  # Khởi động Metro Bundler
Nếu chạy trên Android (có máy ảo hoặc thiết bị thật):

npx react-native run-android
Nếu chạy trên iOS (MacOS + Xcode):

npx react-native run-ios
✅ Ứng dụng React Native sẽ chạy trên điện thoại/máy ảo.

3️⃣ Kiểm tra kết nối giữa React Native và Django
Mở frontend/src/api/authApi.js và kiểm tra API_URL:

const API_URL = 'http://127.0.0.1:8000/api';
Sau đó kiểm tra trong ứng dụng React Native nếu dữ liệu từ Django được hiển thị.


# chạy Backend (Django) và Frontend (React Native) cùng lúc từ thư mục root
# cd vể thư mục root
# npm install concurrently --save-dev

# cấu hình file pakage.json
"scripts": {
    "test": "echo \"Error: no test specified\" && exit 1",
    "start": "concurrently \"npm run server\" \"npm run android\"",
    "server": "cd backend && source venv/bin/activate && python manage.py runserver",
    "android": "cd frontend && npx react-native start",
    "ios": "cd frontend && npx react-native run-ios"
},