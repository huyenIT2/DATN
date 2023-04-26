package com.example.test2

import com.google.gson.annotations.SerializedName

data class Student(
    @SerializedName("msv")
    val list: List<String>
)