import 'package:flutter/material.dart';
import 'package:video_player/video_player.dart';
import 'video_service.dart';
import 'dart:math' as math;

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Miranda Assistant',
      theme: ThemeData.dark(),
      home: const MirandaPage(),
    );
  }
}

class MirandaPage extends StatefulWidget {
  const MirandaPage({Key? key}) : super(key: key);

  @override
  _MirandaPageState createState() => _MirandaPageState();
}

class _MirandaPageState extends State<MirandaPage> {
  Offset _dragPosition = Offset.zero;
  late VideoPlayerController _controller;
  bool _isVideoInitialized = false;
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    _initializeVideo();
  }

  void _initializeVideo() async {
    setState(() {
      _isLoading = true;
    });

    try {
      final videoUrl = await VideoService.generateVideo("Default prompt for avatar");
      _controller = VideoPlayerController.network(videoUrl)
        ..initialize().then((_) {
          setState(() {
            _isVideoInitialized = true;
            _isLoading = false;
          });
          _controller.play();
          _controller.setLooping(true);
        });
    } catch (e) {
      print('Failed to generate video: $e');
      setState(() {
        _isLoading = false;
      });
    }
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: GestureDetector(
        onPanUpdate: (details) {
          setState(() {
            _dragPosition = details.localPosition;
          });
        },
        child: SafeArea(
          child: Column(
            children: [
              Padding(
                padding: const EdgeInsets.all(16.0),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                      decoration: BoxDecoration(
                        color: Colors.grey[900],
                        borderRadius: BorderRadius.circular(20),
                      ),
                      const SizedBox(height: 20),
                    Transform(
                      transform: Matrix4.identity()
                        ..setEntry(3, 2, 0.001)
                        ..rotateY(_calculateRotationY(context))
                        ..rotateX(_calculateRotationX(context)),
                      alignment: FractionalOffset.center,
                      child: Stack(
                        children: [
                          if (_isLoading)
                            Container(
                              width: 270,
                              height: 270,
                              color: Colors.black,
                              child: Center(child: CircularProgressIndicator()),
                            )
                          else if (_isVideoInitialized)
                            SizedBox(
                              width: 270,
                              height: 270,
                              child: VideoPlayer(_controller),
                            )
                          else
                            Image.network(
                              'https://cdn.prod.website-files.com/65e89895c5a4b8d764c0d70e/662b9d36e383c902d2fc7874_thumbnail_%252880%2529.webp',
                              width: 270,
                              height: 270,
                              fit: BoxFit.cover,
                            ),
                          Positioned(
                            bottom: 0,
                            left: 0,
                            right: 0,
                            height: 135,
                            child: Container(
                              decoration: BoxDecoration(
                                gradient: LinearGradient(
                                  begin: Alignment.bottomCenter,
                                  end: Alignment.topCenter,
                                  colors: [
                                    Colors.black.withOpacity(0.9),
                                    Colors.transparent,
                                  ],
                                ),
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                      
                      
                      child: Row(
                        children: const [
                          Icon(Icons.circle, color: Colors.green, size: 12),
                          SizedBox(width: 4),
                          Text('77%', style: TextStyle(color: Colors.white)),
                        ],
                      ),
                    ),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                      decoration: BoxDecoration(
                        color: Colors.grey[900],
                        borderRadius: BorderRadius.circular(20),
                        border: Border.all(color: Colors.white30, width: 1),
                      ),
                      child: const Text('Switch to chat', style: TextStyle(color: Colors.white)),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 20),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: const [
                  Icon(Icons.arrow_back, color: Colors.white),
                  Column(
                    children: [
                      Text('Miranda', style: TextStyle(fontSize: 21, fontWeight: FontWeight.normal, color: Colors.white)),
                      SizedBox(height: 1),
                      Text('secretary', style: TextStyle(color: Colors.grey, fontSize: 15)),
                    ],
                  ),
                  Icon(Icons.arrow_forward, color: Colors.white),
                ],
              ),
              const SizedBox(height: 20),
              Transform(
                transform: Matrix4.identity()
                  ..setEntry(3, 2, 0.001)
                  ..rotateY(_calculateRotationY(context))
                  ..rotateX(_calculateRotationX(context)),
                alignment: FractionalOffset.center,
                child: Stack(
                  children: [
                    Image.network(
                      'https://cdn.prod.website-files.com/65e89895c5a4b8d764c0d70e/662b9d36e383c902d2fc7874_thumbnail_%252880%2529.webp',
                      width: 270,
                      height: 270,
                      fit: BoxFit.cover,
                    ),
                    Positioned(
                      bottom: 0,
                      left: 0,
                      right: 0,
                      height: 135,
                      child: Container(
                        decoration: BoxDecoration(
                          gradient: LinearGradient(
                            begin: Alignment.bottomCenter,
                            end: Alignment.topCenter,
                            colors: [
                              Colors.black.withOpacity(0.9),
                              Colors.transparent,
                            ],
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
              const Spacer(),
              const Padding(
                padding: EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text('Try Asking', style: TextStyle(color: Colors.white70)),
                    SizedBox(height: 8),
                    Text('→ how productive do you think I was today?', style: TextStyle(color: Colors.white30)),
                    Text('→ what meetings should I be prep for tomorrow?', style: TextStyle(color: Colors.white30)),
                    Text('→ do I need to follow up with anyone', style: TextStyle(color: Colors.white30)),
                  ],
                ),
              ),
              Padding(
                padding: const EdgeInsets.all(16.0),
                child: Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: Colors.grey[900],
                    borderRadius: BorderRadius.circular(30),
                  ),
                  child: const Center(
                    child: Icon(Icons.mic, color: Colors.white),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  double _calculateRotationY(BuildContext context) {
    double screenWidth = MediaQuery.of(context).size.width;
    return ((_dragPosition.dx / screenWidth) - 0.5) * 0.5;
  }

  double _calculateRotationX(BuildContext context) {
    double screenHeight = MediaQuery.of(context).size.height;
    return -((_dragPosition.dy / screenHeight) - 0.5) * 0.5;
  }
}