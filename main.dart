import 'package:flutter/material.dart';
import 'screens/home_screen.dart';

void main() {
  runApp(const CodeKApp());
}

class CodeKApp extends StatelessWidget {
  const CodeKApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'CodeK',
      theme: ThemeData(useMaterial3: true),
      home: const HomeScreen(),
    );
  }
}
