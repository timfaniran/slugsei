import React, { useState } from 'react';
import { Box, Typography, Card, Button, TextField } from '@mui/material';
import Header from './Header';

const buttonStyles = {
  backgroundColor: '#BA0C2F',
  fontSize: '1rem',
  fontWeight: 'bold',
  borderRadius: '50px',
  fontFamily: "'Roboto', sans-serif",
  color: '#FFFFFF',
  textTransform: 'uppercase',
  padding: '0.5rem 1.5rem',
  '&:hover': {
    backgroundColor: '#A11222',
  },
};

const SlugSeiPage = () => {
  const [video, setVideo] = useState(null); // State for uploaded video
  const [showStats, setShowStats] = useState(false); // State to control stats visibility
  const [chatMessages, setChatMessages] = useState([
    { sender: 'AI', message: 'Welcome! How can I assist you with your baseball coaching today?' },
  ]);
  const [inputMessage, setInputMessage] = useState('');

  const handleVideoUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const videoURL = URL.createObjectURL(file);
      setVideo(videoURL);
      setShowStats(false); // Reset stats visibility on new upload
    }
  };

  const handleAnalyzeVideo = () => {
    if (video) {
      setShowStats(true);
    }
  };

  const handleSendMessage = () => {
    if (inputMessage.trim()) {
      setChatMessages((prev) => [
        ...prev,
        { sender: 'User', message: inputMessage },
        { sender: 'AI', message: "That's great! Let's dive deeper into your game stats." },
      ]);
      setInputMessage('');
    }
  };

  return (
    <>
      {/* Header */}
      <Header />

      {/* Main Content */}
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'row',
          gap: 4,
          px: 4,
          py: 3,
          backgroundColor: '#F4F4F4',
          height: 'calc(100vh - 80px)', // Adjust height considering the header
          overflow: 'auto',
        }}
      >
        {/* Video Upload Section */}
        <Box
          sx={{
            flex: 2,
            backgroundColor: '#D1E8FF',
            padding: '1.5rem',
            borderRadius: '16px',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            alignItems: 'center',
            boxShadow: '0px 4px 20px rgba(0, 0, 0, 0.1)',
          }}
        >
          {video ? (
            <video
              src={video}
              controls
              style={{
                width: '100%',
                height: '100%',
                objectFit: 'cover',
                borderRadius: '12px',
              }}
            />
          ) : (
            <Box
              sx={{
                width: '100%',
                height: '100%',
                border: '2px dashed #999',
                borderRadius: '12px',
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
              }}
            >
              <Typography variant="h6" sx={{ color: '#555' }}>
                Upload a video
              </Typography>
            </Box>
          )}
          <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
            <Button
              variant="contained"
              component="label"
              sx={buttonStyles}
            >
              Upload Video
              <input
                type="file"
                accept="video/*"
                hidden
                onChange={handleVideoUpload}
              />
            </Button>
            <Button
              variant="contained"
              sx={buttonStyles}
              onClick={handleAnalyzeVideo}
              disabled={!video}
            >
              Analyze Video
            </Button>
          </Box>
        </Box>

        {/* AI Assistant Coaching Chatbot */}
        <Box
          sx={{
            flex: 1,
            backgroundColor: '#FFE5D9',
            padding: '1.5rem',
            borderRadius: '16px',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between',
            boxShadow: '0px 4px 20px rgba(0, 0, 0, 0.1)',
            height: '90%',
          }}
        >
          {/* Chat Bubbles */}
          <Box
            sx={{
              flex: 1,
              overflowY: 'auto',
              mb: 2,
              padding: '1rem',
              backgroundColor: '#FFFFFF',
              borderRadius: '12px',
              boxShadow: '0px 2px 10px rgba(0, 0, 0, 0.1)',
            }}
          >
            {chatMessages.map((msg, idx) => (
              <Box
                key={idx}
                sx={{
                  display: 'flex',
                  justifyContent: msg.sender === 'AI' ? 'flex-start' : 'flex-end',
                  marginBottom: '1rem',
                }}
              >
                <Box
                  sx={{
                    maxWidth: '60%',
                    backgroundColor: msg.sender === 'AI' ? '#E0F7FA' : '#BA0C2F',
                    color: msg.sender === 'AI' ? '#333' : '#FFFFFF',
                    padding: '0.8rem 1rem',
                    borderRadius: msg.sender === 'AI' ? '16px 16px 16px 0px' : '16px 16px 0px 16px',
                    boxShadow: '0px 2px 5px rgba(0, 0, 0, 0.1)',
                  }}
                >
                  <Typography
                    variant="body1"
                    sx={{
                      fontFamily: "'Roboto', sans-serif",
                      fontSize: '1rem',
                    }}
                  >
                    {msg.message}
                  </Typography>
                </Box>
              </Box>
            ))}
          </Box>

          {/* Input Section */}
          <Box sx={{ display: 'flex', gap: 1 }}>
            <TextField
              variant="outlined"
              fullWidth
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder="Type your message..."
              sx={{ backgroundColor: '#FFFFFF', borderRadius: '8px' }}
            />
            <Button
              variant="contained"
              sx={buttonStyles}
              onClick={handleSendMessage}
            >
              Send
            </Button>
          </Box>
        </Box>
      </Box>

      {/* Stat Analyze Section */}
      {showStats && (
        <Box
          sx={{
            display: 'flex',
            justifyContent: 'space-between',
            px: 4,
            py: 4,
            gap: 4,
          }}
        >
          {[1, 2, 3].map((_, idx) => (
            <Card
              key={idx}
              sx={{
                flex: 1,
                backgroundColor: '#FEE8D4',
                padding: '1.5rem',
                borderRadius: '12px',
                textAlign: 'center',
                boxShadow: '0px 4px 20px rgba(0, 0, 0, 0.1)',
              }}
            >
              <Typography
                variant="h6"
                sx={{
                  fontFamily: "'Roboto', sans-serif",
                  fontWeight: 'bold',
                }}
              >
                Stat Analyze
              </Typography>
            </Card>
          ))}
        </Box>
      )}
    </>
  );
};

export default SlugSeiPage;
