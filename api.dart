import 'dart:convert';
import 'package:http/http.dart' as http;

class CodeKApi {
  final String baseUrl;

  CodeKApi({this.baseUrl = 'http://127.0.0.1:8000'});

  Future<Map<String, dynamic>> run(String prompt) async {
    final response = await http.post(
      Uri.parse('$baseUrl/run'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'prompt': prompt}),
    );

    if (response.statusCode != 200) {
      throw Exception('Request failed: ${response.body}');
    }
    return jsonDecode(response.body) as Map<String, dynamic>;
  }
}
