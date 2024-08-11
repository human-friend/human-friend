import 'dart:convert';
import 'package:http/http.dart' as http;

class VideoService {
  static const String baseUrl = "http://127.0.0.1:8000";

  static Future<String> generateVideo(String prompt) async {
    final response = await http.post(
      Uri.parse('$baseUrl/generate_video'),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: jsonEncode(<String, String>{'prompt': prompt}),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return data['video_url'];
    } else {
      throw Exception('Failed to generate video');
    }
  }
}