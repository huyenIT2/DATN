package com.example.test2;

import okhttp3.MultipartBody;
import retrofit2.Call;
import retrofit2.http.Multipart;
import retrofit2.http.POST;
import retrofit2.http.Part;

public interface Api_Service {
    @Multipart
    @POST("/predict")
    Call<Student> post_img(
            @Part MultipartBody.Part image
    );
}
