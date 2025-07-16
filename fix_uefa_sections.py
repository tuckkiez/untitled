#!/usr/bin/env python3
"""
Fix UEFA Champions League sections to match the format of other matches
"""

def fix_uefa_sections():
    """Replace UEFA sections with proper 4-section format"""
    
    # Read the current index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the start of UEFA section
    uefa_start = content.find('<!-- Match 4: Dinamo Minsk vs Ludogorets -->')
    if uefa_start == -1:
        print("❌ UEFA section not found!")
        return False
    
    # Find the end of UEFA section (before footer)
    footer_start = content.find('<div class="footer">')
    if footer_start == -1:
        print("❌ Footer not found!")
        return False
    
    # Extract content before and after UEFA section
    before_uefa = content[:uefa_start]
    after_uefa = content[footer_start:]
    
    # Create new UEFA sections with proper format
    uefa_sections = '''                <!-- Match 4: Dinamo Minsk vs Ludogorets -->
                <div class="match-card">
                    <div class="league-badge">🏆 UEFA Champions League</div>
                    
                    <div class="match-teams">
                        <span class="team-name">Dinamo Minsk</span>
                        <span class="vs">VS</span>
                        <span class="team-name">Ludogorets</span>
                    </div>
                    
                    <div class="match-info">
                        <div class="info-item">
                            <span class="info-icon">⏰</span>
                            <span>01:45 Thai Time</span>
                        </div>
                        <div class="info-item">
                            <span class="info-icon">🏟️</span>
                            <span>Városi Stadion</span>
                        </div>
                        <div class="info-item">
                            <span class="info-icon">🎯</span>
                            <span>1st Qualifying Round</span>
                        </div>
                        <div class="info-item">
                            <span class="info-icon">📊</span>
                            <span>14+ Bookmakers</span>
                        </div>
                    </div>
                    
                    <div class="predictions-grid">
                        <div class="prediction-section match-result-section">
                            <div class="prediction-title">
                                <span class="icon">🏆</span>
                                Match Result
                            </div>
                            <div class="prediction-item">
                                <span class="prediction-label">Away Win</span>
                                <span class="prediction-value high-confidence">60.4%</span>
                            </div>
                            <div class="prediction-item">
                                <span class="prediction-label">Draw</span>
                                <span class="prediction-value medium-confidence">26.5%</span>
                            </div>
                            <div class="prediction-item">
                                <span class="prediction-label">Home Win</span>
                                <span class="prediction-value low-confidence">21.2%</span>
                            </div>
                            <div class="prediction-item">
                                <span class="prediction-label">Best Bet</span>
                                <span class="prediction-value high-confidence">Ludogorets Win</span>
                            </div>
                        </div>
                        
                        <div class="prediction-section goals-section">
                            <div class="prediction-title">
                                <span class="icon">⚽</span>
                                Goals Analysis
                            </div>
                            <div class="prediction-item">
                                <span class="prediction-label">Total Goals</span>
                                <span class="prediction-value">2.3</span>
                            </div>
                            <div class="prediction-item">
                                <span class="prediction-label">Over 2.5 Goals</span>
                                <span class="prediction-value medium-confidence">51.9%</span>
                            </div>
                            <div class="prediction-item">
                                <span class="prediction-label">Both Teams Score</span>
                                <span class="prediction-value medium-confidence">52.8%</span>
                            </div>
                            <div class="prediction-item">
                                <span class="prediction-label">Best Bet</span>
                                <span class="prediction-value medium-confidence">Under 2.5 (54%)</span>
                            </div>
                        </div>
                        
                        <div class="prediction-section corner-section">
                            <div class="prediction-title">
                                <span class="icon">🚩</span>
                                Corner Analysis
                            </div>
                            <div class="prediction-item">
                                <span class="prediction-label">Total Expected</span>
                                <span class="prediction-value">10.2</span>
                            </div>
                            <div class="prediction-item">
                                <span class="prediction-label">Over 9.5 Corners</span>
                                <span class="prediction-value medium-confidence">56.7%</span>
                            </div>
                            <div class="prediction-item">
                                <span class="prediction-label">Home Corners</span>
                                <span class="prediction-value">4.8</span>
                            </div>
                            <div class="prediction-item">
                                <span class="prediction-label">Away Corners</span>
                                <span class="prediction-value">5.4</span>
                            </div>
                        </div>
                        
                        <div class="prediction-section handicap-section">
                            <div class="prediction-title">
                                <span class="icon">⚖️</span>
                                Handicap & Value
                            </div>
                            <div class="prediction-item">
                                <span class="prediction-label">Asian Handicap</span>
                                <span class="prediction-value">Away -0.5</span>
                            </div>
                            <div class="prediction-item">
                                <span class="prediction-label">Best Odds</span>
                                <span class="prediction-value high-confidence">1.70 Away</span>
                            </div>
                            <div class="prediction-item">
                                <span class="prediction-label">Value Bet</span>
                                <span class="prediction-value high-confidence">+11.3% Home</span>
                            </div>
                            <div class="prediction-item">
                                <span class="prediction-label">Confidence</span>
                                <span class="prediction-value high-confidence">High (60%)</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Match 5: Linfield vs Shelbourne -->
                <div class="match-card">
                    <div class="league-badge">🏆 UEFA Champions League</div>
                    
                    <div class="match-teams">
                        <span class="team-name">Linfield</span>
                        <span class="vs">VS</span>
                        <span class="team-name">Shelbourne</span>
                    </div>
                    
                    <div class="match-info">
                        <div class="info-item">
                            <span class="info-icon">⏰</span>
                            <span>01:45 Thai Time</span>
                        </div>
                        <div class="info-item">
                            <span class="info-icon">🏟️</span>
                            <span>Windsor Park</span>
                        </div>
                        <div class="info-item">
                            <span class="info-icon">🎯</span>
                            <span>1st Qualifying Round</span>
                        </div>
                        <div class="info-item">
                            <span class="info-icon">🏴󠁧󠁢󠁮󠁩󠁲󠁿</span>
                            <span>Belfast, N. Ireland</span>
                        </div>
                    </div>
                    
                    <div class="predictions-grid">
                        <div class="prediction-section match-result-section">
                            <div class="prediction-title">
                                <span class="icon">🏆</span>
                                Match Result
                            </div>
                            <div class="prediction-item">
                                <span class="prediction-label">Home Win</span>
                                <span class="prediction-value medium-confidence">52.0%</span>
                            </div>
                            <div class="prediction-item">
                                <span class="prediction-label">Draw</span>
                                <span class="prediction-value medium-confidence">28.5%</span>
                            </div>
                            <div class="prediction-item">
                                <span class="prediction-label">Away Win</span>
                                <span class="prediction-value low-confidence">19.5%</span>
                            </div>
                            <div class="prediction-item">
                                <span class="prediction-label">Best Bet</span>
                                <span class="prediction-value medium-confidence">Linfield Win</span>
                            </div>
                        </div>
                        
                        <div class="prediction-section goals-section">
                            <div class="prediction-title">
                                <span class="icon">⚽</span>
                                Goals Analysis
                            </div>
                            <div class="prediction-item">
                                <span class="prediction-label">Total Goals</span>
                                <span class="prediction-value">2.1</span>
                            </div>
                            <div class="prediction-item">
                                <span class="prediction-label">Over 2.5 Goals</span>
                                <span class="prediction-value low-confidence">34.8%</span>
                            </div>
                            <div class="prediction-item">
                                <span class="prediction-label">Both Teams Score</span>
                                <span class="prediction-value low-confidence">41.7%</span>
                            </div>
                            <div class="prediction-item">
                                <span class="prediction-label">Best Bet</span>
                                <span class="prediction-value high-confidence">Under 2.5 (65%)</span>
                            </div>
                        </div>
                        
                        <div class="prediction-section corner-section">
                            <div class="prediction-title">
                                <span class="icon">🚩</span>
                                Corner Analysis
                            </div>
                            <div class="prediction-item">
                                <span class="prediction-label">Total Expected</span>
                                <span class="prediction-value">8.5</span>
                            </div>
                            <div class="prediction-item">
                                <span class="prediction-label">Over 8.5 Corners</span>
                                <span class="prediction-value medium-confidence">47.7%</span>
                            </div>
                            <div class="prediction-item">
                                <span class="prediction-label">Home Corners</span>
                                <span class="prediction-value">4.2</span>
                            </div>
                            <div class="prediction-item">
                                <span class="prediction-label">Away Corners</span>
                                <span class="prediction-value">4.3</span>
                            </div>
                        </div>
                        
                        <div class="prediction-section handicap-section">
                            <div class="prediction-title">
                                <span class="icon">⚖️</span>
                                Handicap & Value
                            </div>
                            <div class="prediction-item">
                                <span class="prediction-label">Asian Handicap</span>
                                <span class="prediction-value">Home -0.25</span>
                            </div>
                            <div class="prediction-item">
                                <span class="prediction-label">Home Advantage</span>
                                <span class="prediction-value high-confidence">Strong</span>
                            </div>
                            <div class="prediction-item">
                                <span class="prediction-label">European Experience</span>
                                <span class="prediction-value medium-confidence">Linfield Edge</span>
                            </div>
                            <div class="prediction-item">
                                <span class="prediction-label">Confidence</span>
                                <span class="prediction-value medium-confidence">Medium (52%)</span>
                            </div>
                        </div>
                    </div>
                </div>
           
            </div>
        </div>
        
        '''
    
    # Combine all parts
    new_content = before_uefa + uefa_sections + after_uefa
    
    # Write the new content
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ UEFA sections updated successfully!")
    print("🏆 Both matches now have proper 4-section format:")
    print("   • Match Result")
    print("   • Goals Analysis") 
    print("   • Corner Analysis")
    print("   • Handicap & Value")
    
    return True

if __name__ == "__main__":
    success = fix_uefa_sections()
    if success:
        print("\n🎯 Ready to view updated website!")
    else:
        print("\n❌ Failed to update UEFA sections")
