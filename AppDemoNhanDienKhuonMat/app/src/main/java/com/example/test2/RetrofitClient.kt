package com.example.test2

import okhttp3.OkHttpClient
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.util.concurrent.TimeUnit

object RetrofitClient {
    const val BASE_URL = "http://172.72.213.234:6868/"
    const val READ_TIME_OUT = 15L
    const val CONNECT_TIME_OUT = 15L
    var INSTANCE: Retrofit? = null
    fun getInstance(): Retrofit {
        return INSTANCE ?: synchronized(this) {
            INSTANCE ?: retrofitBuilder().also {
                INSTANCE = it
            }
        }
    }

    private fun retrofitBuilder(): Retrofit {
        val client: OkHttpClient = OkHttpClient.Builder()
            .readTimeout(READ_TIME_OUT, TimeUnit.SECONDS)
            .connectTimeout(CONNECT_TIME_OUT, TimeUnit.SECONDS)
            .build()
        return Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .client(client)
            .build()
    }
}