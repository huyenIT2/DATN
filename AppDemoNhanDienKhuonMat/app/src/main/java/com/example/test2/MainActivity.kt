package com.example.test2

import android.content.ContentValues
import android.content.Intent
import android.graphics.Bitmap
import android.net.Uri
import android.os.Bundle
import android.provider.MediaStore
import android.util.Log
import android.view.View
import android.widget.Toast
import androidx.activity.result.ActivityResultCallback
import androidx.activity.result.contract.ActivityResultContracts.StartActivityForResult
import androidx.appcompat.app.AppCompatActivity
import com.example.test2.databinding.ActivityMainBinding
import okhttp3.MediaType
import okhttp3.MultipartBody
import okhttp3.RequestBody
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import java.io.File
import java.io.IOException


class MainActivity : AppCompatActivity() {
    private var muri: Uri? = null
    private val binding by lazy {
        ActivityMainBinding.inflate(layoutInflater)
    }
    private val apiService by lazy {
        RetrofitClient.getInstance().create(Api_Service::class.java)
    }
    private var bitmap: Bitmap? = null
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(binding.root)

        binding.btnPickImage.setOnClickListener { v: View? ->
//            val cameraIntent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)
//            startActivityForResult(cameraIntent, REQUEST_CODE_CAMERA)
            openGallery()
        }
        binding.btnCamera.setOnClickListener {
            val fileName = "new-photo-name.jpg"
            // Create parameters for Intent with filename
            // Create parameters for Intent with filename
            val values = ContentValues()
            values.put(MediaStore.Images.Media.TITLE, fileName)
            values.put(MediaStore.Images.Media.DESCRIPTION, "Image capture by camera")
            muri = contentResolver.insert(
                MediaStore.Images.Media.EXTERNAL_CONTENT_URI,
                values
            )
            val intent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)
            intent.putExtra(MediaStore.EXTRA_OUTPUT, muri)
            startActivityForResult(intent, 1231)
        }
        binding.btnRetry.setOnClickListener {
            callAPI()
        }
    }

    @Deprecated("Deprecated in Java")
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode == 1231 && resultCode == RESULT_OK) {
            try {
                val cr = contentResolver
                try {
                    // Creating a Bitmap with the image Captured
                    val bitmap = MediaStore.Images.Media.getBitmap(cr, muri)
                    // Setting the bitmap as the image of the
                    binding.clickImage.setImageBitmap(bitmap)
                    callAPI()
                } catch (e: IOException) {
                    e.printStackTrace()
                }
            } catch (e: IllegalArgumentException) {
                if (e.message != null) Log.e("Exception", e.message!!) else Log.e(
                    "Exception",
                    "Exception"
                )
                e.printStackTrace()
            }
        }
    }

    companion object {
        private const val REQUEST_CODE_CAMERA = 123
    }

    private fun openGallery() {
        val intent = Intent()
        intent.type = "image/*"
        intent.action = Intent.ACTION_GET_CONTENT
        mActivityResultLauncher.launch(Intent.createChooser(intent, "Select AVT"))
    }

    private val mActivityResultLauncher = registerForActivityResult(
        StartActivityForResult(),
        ActivityResultCallback { result ->
            Log.e("activity", "onActivityResult")
            if (result.resultCode == RESULT_OK) {
                val data: Intent = result.data ?: return@ActivityResultCallback
                val uri = data.data
                muri = uri
                try {
                    val bitmap =
                        MediaStore.Images.Media.getBitmap(binding.root.context.contentResolver, uri)
                    binding.clickImage.background = null
                    binding.clickImage.setImageBitmap(bitmap)
                    callAPI()
                } catch (e: IOException) {
                    e.printStackTrace()
                }
            }
        }
    )

    private fun callAPI() {
        showLoading()
//        onClickRequestPermission();
        val strRealPath: String = RealPathUtil.getRealPath(this, muri)
        val file = File(strRealPath)
        val requestBodyimg = RequestBody.create(MediaType.parse("multipart/from-data"), file)
        val multipartBody = MultipartBody.Part.createFormData("image", file.name, requestBodyimg)
        println("call")
        apiService.post_img(multipartBody).enqueue(object : Callback<Student?> {
            override fun onResponse(call: Call<Student?>, response: Response<Student?>) {
                hideLoading()
                binding.btnRetry.visibility = View.GONE
                /*Intent intent = new Intent(MainActivity.this, AnsActivity.class);
                intent.putExtra("ans",response.toStudent());
                startActivity(intent);*/
                Log.d("call_api", "onResponse: $response")
                response.body()?.let {
                    val rs = it.list.find { item -> item.length > 5 } ?: "Cannot find this student"
                    binding.tvStudentCode.text = rs.toString()
                }
            }

            override fun onFailure(call: Call<Student?>, t: Throwable) {
                hideLoading()
                Toast.makeText(this@MainActivity, "Lỗi", Toast.LENGTH_SHORT).show()
                binding.tvStudentCode.text = t.message
                binding.btnRetry.visibility = View.VISIBLE
                Log.d("call_api", "onResponse: ${t.message}")
            }
        })
    }

    private fun showLoading() {
        binding.loading.visibility = View.VISIBLE
        binding.tvStudentCode.text = ""
    }

    private fun hideLoading() {
        binding.loading.visibility = View.INVISIBLE
    }
}
